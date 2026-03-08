# Changelog

## [0.11.2](https://github.com/pipe-works/pipeworks_entity_state_generation/compare/pipeworks-conditional-axis-v0.11.1...pipeworks-conditional-axis-v0.11.2) (2026-03-08)


### Features

* **api:** add entity state FastAPI service with tests and docs ([bbaffa3](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/bbaffa387bf65c0f165ee78ae6a22aa4d4c73ada))
* **api:** add entity state FastAPI service, tests, and docs ([c85a21b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/c85a21b0a59a13895f21d5208f16bcd65dde12c0))
* **condition-axis:** align canonical labels and lock api metadata parity ([798c508](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/798c5085f05ab6e49746fce01c4d964ae99578c0))
* **condition-axis:** align canonical labels and lock API metadata parity ([8bb9b79](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/8bb9b799fb416dd9972ae6088d7effaf99f34f3f))


### Documentation

* add repository contributor guidelines ([9fa0f17](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/9fa0f176cb8971b78741bba215d91c47c0ae56a2))
* add repository contributor guidelines ([d81c930](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/d81c9301a6b921d8800b38a9c735971821f15c60))

## [0.11.1](https://github.com/pipe-works/pipeworks_entity_state_generation/compare/pipeworks-conditional-axis-v0.11.0...pipeworks-conditional-axis-v0.11.1) (2026-01-27)


### Bug Fixes

* **packaging:** exclude __pycache__ from distribution ([#6](https://github.com/pipe-works/pipeworks_entity_state_generation/issues/6)) ([dd9763b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/dd9763b1d65e0e3fbdb85474f804f5a19357f80e))

## [0.11.0](https://github.com/pipe-works/pipeworks_entity_state_generation/compare/pipeworks-conditional-axis-v0.10.1...pipeworks-conditional-axis-v0.11.0) (2026-01-26)


### ⚠ BREAKING CHANGES

* Removed deprecated/legacy code - clean break

### Features

* Adopt organization-wide standards and reusable CI workflow ([fef535f](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/fef535f4f6daa1cf3d76fdd0c8100201a46af907))
* **ci:** add release automation workflows ([#3](https://github.com/pipe-works/pipeworks_entity_state_generation/issues/3)) ([930f439](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/930f43932e773461dd8d0c5e9af4a57cdb19fa11))
* **ci:** add workflow_dispatch trigger to release-please ([8c87d8b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/8c87d8b19e5aa780ad0d75f62e64975805e2773e))
* Enable documentation builds in CI ([230e70b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/230e70b7a8d44d619e6b69c85af12dade7125155))
* integrate facial signals into character conditions system ([0eed1e0](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/0eed1e008d2f6a70da87ccf78074da9205552628))
* update examples for unified facial signal API (Section 4) ([d2560e4](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/d2560e4e543f34844814b5b032649957c6cedaca))
* Upgrade to enhanced organization pre-commit standards ([71bf5e7](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/71bf5e79c1108c88a3d2bf19be437c9dd48ccef2))


### Bug Fixes

* Add VSCode workspace settings to suppress YAML validation errors ([b7ad1aa](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/b7ad1aaa82a0576cc790c5b7aef05e5cbfaf9a99))
* Add yaml-language-server disable comments for custom environments ([f7e14f2](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/f7e14f28b2c5501921ba15585950437fad245fab))
* Apply black 26.1.0 formatting to examples directory ([9c03037](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/9c03037cbd9b6f9f3d089978f98b5a8742a2a4ff))
* **ci:** add required permissions to release-please workflow ([2abc270](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/2abc27028731d4f9dc63a35928bf430ed19be194))
* **ci:** add security-events permission for CodeQL ([39fab9a](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/39fab9a02cd342ad0fcf6395659350607b17b100))
* Disable YAML schema validation for publish.yml ([3c2a230](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/3c2a23013750476b4e161e5c482103495b7e6c85))
* **pre-commit:** correct hook execution order ([98734f8](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/98734f8271995fe76e0e78f49b9010667f604eeb))
* remove duplicate Design & Philosophy from navigation tree ([75bb9ba](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/75bb9ba20d0e9964e2fa259a8449ec6a87df073c))
* Remove environment blocks causing schema validation errors ([d4838a8](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/d4838a800d53f1f6cd05a0da52e4211de1d67bf3))
* resolve Sphinx build warnings in documentation ([ceba1a7](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ceba1a79ba10e0128aa761f00478602b1d9fa9f8))
* update all examples and tests to use unified API only ([5ee4c12](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/5ee4c1203b4dcfa23b2c3ac0a467251507cf613d))
* update GitHub Actions artifact actions to v4 ([748866d](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/748866d6a9d5204806810280a88dd416d00e1342))
* Update README badges and workflow references ([9029801](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/9029801f07d75cc81aafac94fddd56b1ed403a6a))
* Use inline disable-line for yaml-language-server validation ([ed042bd](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ed042bd57a8575076d27c86831a758838409a6a9))
* use isolated RNG instances to prevent global state pollution ([bf2ff4a](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/bf2ff4ad3154558addf3d9afb4038d2da1eab3bb))


### Documentation

* add Architecture Diagrams section to Sphinx toctree ([e27adea](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/e27adea17b08eb38557c4d8deb408c9632f919af))
* add comprehensive merge TODO for facial conditions integration ([0405711](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/0405711a232f72608b93fb3e01285d62901d13c5))
* add comprehensive Pipeworks architecture diagrams ([d712c9d](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/d712c9d4fd6cc5d28a5721aee14d34954ee2cd22))
* add comprehensive usage examples and tests ([7fe1fbe](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/7fe1fbea71f2043a35d8a8916d9ee0629f384f50))
* add Sphinx documentation and ReadTheDocs integration ([ea8fa92](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ea8fa92ce79d6c99e31cbe263a0958838fda50ac))
* complete Phase 2 API reference documentation ([ff77509](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ff7750916bad2cee603e92c9160c4dbe0603b45a))
* complete Section 5 - Documentation Updates ([0a3a102](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/0a3a102ddb52eae5428270079d5a209d4b9f91cc))
* complete Section 8 (Risk Mitigation) - merge 100% complete ([b7e0f09](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/b7e0f09f50c46dfa873a5bba34025eefd3141e37))
* establish baseline API documentation for backward compatibility ([6587a7b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/6587a7b6110196707f88e22998d7f19daca3c452))
* fix broken links and remove deprecated API references ([2150c8d](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/2150c8df80df0369ef35e35d59f939d88d7f3f3e))
* fix external file links and suppress MyST warnings ([63e3f80](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/63e3f802bf0f617dea277d359f4638e6c5d5daea))
* fix README to reflect Sphinx autodoc migration ([624b1fb](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/624b1fbb672044e17d72e189ce6531b9d0a54351))
* fix Sphinx cross-reference warnings ([5fef882](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/5fef8826dea0b981dee8e1904c1113548cd90549))
* fix TODO list organization and add comprehensive examples README ([438b5b4](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/438b5b4441c125198ae67d557f41bde8d100fc6a))
* housekeeping - complete Phase 2, add examples to Sphinx ([c5f5d66](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/c5f5d666e4ba8be01cbdcdd05369ab93c66085ad))
* mark all Section 5 subtask checkboxes complete ([634c264](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/634c26440da132a1bbfb6ac06537bbc043337536))
* mark Section 4 complete in merge_todo.md (69% complete) ([6a48c79](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/6a48c794ab0946e933f45db5eda2d5501189a3c2))
* mark Section 5 complete in merge_todo.md (90% complete) ([ddf97bc](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ddf97bcae9080ef2b9ff87b7af7e1f1018cc8948))
* mark Section 6 (Verification & Testing) complete ([baf5eb5](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/baf5eb5803444a444b6f1f536da24e90577d1fd0))
* mark Section 7 complete in merge_todo.md (97% complete) ([5cc4809](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/5cc4809c679e6589d5fa340045b05f763542b1fb))
* mark Sections 2 & 3 tasks complete in merge_todo.md ([271bb4e](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/271bb4e73718d79842e4bf1202cb3a62ca73cd17))
* migrate to Sphinx autodoc for zero-maintenance documentation ([ce8abcb](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ce8abcb11dc08586877c834a799d3eae83bb8852))
* remove design_philosophy directory from documentation ([127cacf](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/127cacf6d2a629c0d4b3d6b3e49174b85ddaf82e))
* restructure design documentation with clearer hierarchy ([016789b](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/016789bb4cf4c9d1508f9b4ee4194573c7167bdf))
* restructure Sphinx navigation for improved usability and stability ([1a5176a](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/1a5176a2d798a3f270e18bd709e66134e898df4b))
* rewrite examples README for clarity and accuracy ([679bdb4](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/679bdb40d30b71cefb3122ddb77a96ab34dc03c3))
* streamline and reorganize design documentation ([8320c7f](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/8320c7fc8208c6af02fe8ef57bcda7683c9bf455))
* strip to auto-generated API reference only ([ab5778e](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ab5778e2e62095c9367795f42a765dbe5f70fca1))
* update all documentation for v1.1.0 unified API ([5d042d0](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/5d042d0bfc3c874958d76a90130334dbee4d731c))
* update main README with architecture diagram references ([ccd478f](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/ccd478f72642558fed007e7a6c8e953210e8ff6b))
* update merge_todo.md with progress (60% complete) ([cc0d67c](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/cc0d67c06abaef5b603b765b64bfb1a9bd565ffb))
* update README and TODO to reflect docs/ reorganization ([909494c](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/909494ce341507149a684e6f73264b564683cf9e))
* update TODO list and README for completed examples ([6349303](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/6349303c8d03a9ae7b2401e52ed48cab640e9159))


### Code Refactoring

* remove all deprecated facial conditions API (Section 7) ([3ad23e1](https://github.com/pipe-works/pipeworks_entity_state_generation/commit/3ad23e109cfbae4306f72b4be50dffe9b4f72827))
