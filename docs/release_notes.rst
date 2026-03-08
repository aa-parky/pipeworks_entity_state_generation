Release Notes
=============

2026-03-08
----------

Condition-axis contract parity update:

- Added ``generator_version`` and ``generator_capabilities`` to ``POST /api/entity`` responses.
- Aligned canonical label ordering for ``physique`` and ``health`` with mud-server policy.
- Aligned occupation ``visibility`` label spelling to canonical ``discrete``.
- Updated tests to lock metadata and label-order contracts to prevent future drift.
