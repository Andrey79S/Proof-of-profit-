graph LR
    A[Real-world Business<br>(PoP Node)]
    B[Economic Observations<br>(Self-reported + External Signals)]
    C[Consistency & Rule Checks<br>(Non-judgmental Validation)]
    D[On-chain Commitments<br>(Hashes, Timestamps, Metadata)]
    E[DAO Governance<br>(Protocol Rules & Parameters)]
    F[Protocol Policies<br>(Formats, Thresholds, Transparency)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> A

    style A fill:#e6f7ff,stroke:#333
    style B fill:#f0fff0,stroke:#333
    style C fill:#fffbe6,stroke:#333
    style D fill:#e6f7ff,stroke:#333
    style E fill:#fff0e6,stroke:#333
    style F fill:#f5f5f5,stroke:#333
