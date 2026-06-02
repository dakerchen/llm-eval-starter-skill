# Security

Do not publish private examples, customer data, internal project names, credentials, local paths, or proprietary workflow details in eval samples.

Before sharing a package publicly:

1. Replace real customer inputs with synthetic or approved examples.
2. Remove private paths and account names.
3. Remove API keys and environment dumps.
4. Do not include proprietary framework code unless its license allows redistribution.
5. Run:

```bash
python3 scripts/validate_public_package.py
```

Report security issues privately to the repository maintainer.
