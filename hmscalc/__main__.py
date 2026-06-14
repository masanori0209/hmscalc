"""Allow running hmscalc as ``python -m hmscalc``."""

from hmscalc.cli import main

raise SystemExit(main())
