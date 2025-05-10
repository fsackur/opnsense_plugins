<?php

namespace OPNsense\OpenApi\Parsing;

use InvalidArgumentException;
use Attribute;
use ReflectionClass;

#[Attribute]
class Argument
{
    public readonly string $name;
    public readonly string $shortName;
    public readonly bool $isSwitch;
    public readonly string $shortArg;
    public readonly string $longArg;
    public readonly ?string $default;

    public function __construct(string $shortArg, string $longArg, ?string $default = null)
    {
        $this->shortArg = $shortArg;
        $this->longArg = $longArg;
        $this->default = $default;

        $name = str_replace(":", "", $this->longArg);
        $shortName = str_replace(":", "", $this->shortArg);
        $isSwitch = $name === $longArg;
        if ($isSwitch !== ($shortName === $shortArg)) {
            throw new InvalidArgumentException("$longArg and $shortArg have inconsistent colons");
        }
        if ($isSwitch && $default) {
            throw new InvalidArgumentException("Switch $name cannot have default value");
        }
        $this->name = $name;
        $this->shortName = $shortName;
        $this->isSwitch = $isSwitch;
    }
}

class CliOptions
{
    #[Argument("s:", "source-folder:", "/usr/local/opnsense/mvc/app")]
    public readonly string $sourceFolder;

    #[Argument("o:", "output-folder:", __DIR__)]
    public readonly string $outputFolder;

    #[Argument("t", "trace")]
    public readonly bool $trace;

    #[Argument("m", "generate-models")]
    public readonly bool $generateModels;

    #[Argument("g", "generate-schemas")]
    public readonly bool $generateSchemas;

    #[Argument("x", "generate-examples")]
    public readonly bool $generateExamples;
    public readonly string $appDir;
    public readonly string $contribDir;

    private static Self $instance;
    public static function get()
    {
        if (!isset(self::$instance)) {
            self::$instance = new static();
        }
        return self::$instance;
    }

    private function __construct()
    {
        $argProps = [];
        $shortOpts = "";
        $longOpts = [];
        $values = [];
        $class = new ReflectionClass(__CLASS__);
        foreach ($class->getProperties() as $prop) {
            $attrs = $prop->getAttributes();
            if ($attrs) {
                $propName = $prop->name;
                $arg = $attrs[0]->newInstance();

                $longOpts[] = $arg->longArg;
                $argProps[$arg->name] = $propName;
                if ($arg->shortName) {
                    $shortOpts .= $arg->shortArg;
                    $argProps[$arg->shortName] = $propName;
                }

                if ($arg->default !== null) {
                    $values[$propName] = $arg->default;
                } elseif ($arg->isSwitch) {
                    $values[$propName] = false;
                } else {
                    $values[$propName] = new InvalidArgumentException("Parameter $arg->name is mandatory");
                }
            }
        }

        // parse the supplied cli arguments
        $opts = getopt($shortOpts, $longOpts);
        foreach ($opts as $arg => $value) {
            $propName = $argProps[$arg];
            if ($value === false) {
                $value = true;  // PHP weirdness
            }
            $values[$propName] = $value;
        }

        // validate paths
        foreach (["sourceFolder", "outputFolder"] as $prop) {
            $path = realpath($values[$prop]);
            if (!$path) {
                throw new InvalidArgumentException("$prop is not a directory");
            }
            $values[$prop] = $path;
        }

        foreach ($values as $prop => $value) {
            if (gettype($value) == "object") {
                throw $value;
            }
            $this->$prop = $value;
        }

        // walk backwards looking for /mvc/app folder
        $appBase = $this->sourceFolder;
        while ($appBase != "/") {
            $appDir = realpath("$appBase/mvc/app");
            if ($appDir) {
                break;
            }
            $appBase = dirname($appBase);
        }
        if (!$appDir) {
            throw new InvalidArgumentException("Could not find 'mvc/app' folder in any parent of $this->sourceFolder");
        }
        $this->appDir = $appDir;

        $contribBase = $appBase;
        while ($contribBase != "/") {
            $contribDir = realpath("$contribBase/contrib");
            if ($contribDir && realpath("$contribBase/contrib/tzdata/iso3166.tab")) {
                break;
            }
            $contribBase = dirname($contribBase);
        }
        if (!$contribDir) {
            throw new InvalidArgumentException("Could not find 'contrib' folder in any parent of $appDir");
        }
        $this->contribDir = $contribDir;
    }
}

return CliOptions::get();
