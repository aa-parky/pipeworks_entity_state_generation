Release Notes
=============

2026-03-08
----------

Condition-axis contract parity update:

- Added ``generator_version`` and ``generator_capabilities`` to ``POST /api/entity`` responses.
- Added canonical numeric ``axes`` output (``axis -> {label, score}``) while preserving
  existing ``character`` and ``occupation`` label payloads.
- Added ``numeric_axis_scores`` generator capability token for adapter feature detection.
- Aligned canonical label ordering for ``physique`` and ``health`` with mud-server policy.
- Aligned occupation ``visibility`` label spelling to canonical ``discrete``.
- Updated tests to lock metadata, dual-format axis payloads, and label-order contracts.
