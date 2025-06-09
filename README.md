# JaffeBot 3.0

JaffeBot 3.0 is an AI-powered SEO-audit automation interface that streamlines technical, content, and link-profile analysis across large site portfolios. It features a modular, multi-agent architecture (Discovery, Preliminary Audit, Content Refresher, Backlink & Outreach) and integrates with Google Search Console (GSC) and Task Master for execution tracking.

## Features
- Automated technical, content, and backlink audits
- Modular agent-based architecture
- Integration with GSC and Task Master
- Multilingual content generation
- Internal-link suggestions and schema generation

## Project Structure
- `src/` - Source code for agents and core logic
- `tests/` - Automated tests
- `docs/` - Documentation and SOPs
- `config/` - Configuration files

## Getting Started
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd jaffebot
   ```
2. Install dependencies (Python, Node.js, etc. as required)
3. Set up environment variables as described in `.env.example`
4. Run initial setup scripts if provided

## Prerequisites
- Python 3.10+
- Node.js 18+
- Postgres (for audit DB)
- Access to OpenAI API (for content generation)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 
