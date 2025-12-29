graph LR
    A[Real-world Business<br>(PoP Node)] --> B[Off-chain Economic Data<br>(Revenue, Costs, Labor, etc.)]
    B --> C[Verification Layer<br>(Rules, Attestations, Checks)]
    C --> D[Solana Blockchain<br>(Immutable Hashes & Records)]
    D --> E[DAO Governance<br>(Rules, Decisions, Treasury)]
    E -->|Feedback & Policies| A

    style A fill:#e6f7ff,stroke:#333
    style B fill:#f0fff0,stroke:#333
    style C fill:#fffbe6,stroke:#333
    style D fill:#e6f7ff,stroke:#333
    style E fill:#fff0e6,stroke:#333
