graph LR
    A["Daily Operations<br/>(e.g. Pizza Sales)"]
    B["Economic Data Collection<br/>(Raw Observations)"]
    C["Categorization<br/>(Revenue, Ingredients, Labor, Rent and Utilities, Taxes)"]
    D["PoP Standardized Economic Report<br/>(Rule-based Computed Metrics)"]
    E["Consistency and Attestation Checks<br/>(Format, Logic, Provenance)"]
    F["On-chain Commitment<br/>(Hash + Selective Disclosure to Solana)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

    style A fill:#f0fff0,stroke:#333
    style C fill:#fffbe6,stroke:#333
    style F fill:#e6f7ff,stroke:#333
