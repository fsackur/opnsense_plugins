## Done

- [x] parse XML models
- [x] parse endpoints
- [x] identify POST/GET
- [x] identify request bodies
- [x] generated spec passes validation and can be used to generate clients
- [ ] auth module
  - can't get past authentication (maybe I need to be root?)
- [ ] non-model repsonses (e.g. "rows", "result")
  - effort not currently known; looks like regex
  - will _probably_ do
- [ ] model property constraints and qualifiers (e.g. Required, Mask, Default, ValidationMessage)
  - mostly, won't do
  - will do some if low effort (e.g. Required, Default)
- [ ] primitive types
  - currently, all string. Since non-body params are in the path and must be passed as string, this is not critical
  - will do, low effort
- [ ] optional path params
  - will do
  - path params are always required in OpenApi; therefore, each param combination is a separate endpoint
  - 159 endpoints have 1 optional param (+159 endpoints)
  - 8 endpoints have 2 optional params (+24 endpoints)
  - NetworkinsightController has methods with 4, 6, 7 optional params. Hard to do any without doing all, but this is a pain point.
- [ ] configd integration
- [ ] build/test
- [ ] packaging

## Testing

Not done yet. The complete spec is generated and passes validation, except for the Auth module which I can't figure out how to use through raw API calls.

I have generated both python and powershell clients, and verified a couple of endpoints manually.
