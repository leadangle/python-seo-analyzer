# 🔍 SEO Competitor Analyzer

Enhanced version of [python-seo-analyzer](https://github.com/sethblack/python-seo-analyzer) with **competitor analysis** and **keyword gap analysis** features.

![Dashboard](https://via.placeholder.com/800x400/1f77b4/white?text=SEO+Dashboard)

## ✨ Features

### 🆕 New Features
- **📊 Web Dashboard** - Beautiful Streamlit interface
- **📁 CSV Keyword Analysis** - Process Ahrefs keyword exports
- **🔍 Competitor vs Your Site Comparison** - Side-by-side analysis
- **📈 Keyword Gap Analysis** - Find opportunities and quick wins
- **💡 AI-Powered Recommendations** - Actionable SEO insights
- **📋 Export Reports** - JSON reports for further analysis

### 🔧 Original Features
- **Technical SEO Analysis** - Crawl and analyze website structure
- **Content Analysis** - Word count, keyword density, readability
- **On-Page SEO** - Meta tags, headings, images, links
- **AI Content Evaluation** - Using Claude API (optional)
- **Docker Support** - Easy deployment and scaling

## 🚀 Quick Start

### Option 1: Web Dashboard (Recommended)
```bash
# Clone and setup
git clone https://github.com/leadangle/python-seo-analyzer.git
cd python-seo-analyzer
pip install -r requirements.txt

# Launch dashboard
python main.py dashboard
```
Open http://localhost:8501 in your browser.

### Option 2: Command Line Interface
```bash
# Analyze keywords from Ahrefs CSV
python main.py keyword-analysis your-data.csv --output report.json

# Compare competitor vs your site
python main.py compare https://competitor.com https://yoursite.com --csv your-data.csv

# Original SEO analysis
python main.py analyze https://example.com --analyze-headings --analyze-extra-tags
```

### Option 3: Docker
```bash
# Build and run
docker build -t seo-analyzer .
docker run -p 8501:8501 seo-analyzer

# Or use with your CSV data
docker run -v $(pwd):/data -p 8501:8501 seo-analyzer
```

## 📖 Usage Examples

### 1. Analyze Your Ahrefs Data
```bash
# Export keywords from Ahrefs as CSV, then:
python main.py keyword-analysis www.rapidtables.com-keywords.csv

# Output:
📊 Summary Statistics:
  Total Keywords: 2,847
  Total Volume: 2,234,567
  Total Traffic: 156,789
  Average Position: 12.3
  Page 1 Rankings: 234

🏆 Top 10 Keywords by Volume:
   1. notepad                      | Volume:  424,550 | Traffic:   58,525 | Pos:   2.2
   2. online notepad               | Volume:   12,700 | Traffic:    1,970 | Pos:   4.5
   ...
```

### 2. Competitor Analysis
```bash
python main.py compare \
  https://www.rapidtables.com/tools/notepad.html \
  https://appoftheday.com/notepad/ \
  --csv competitor-keywords.csv \
  --output comparison-report.json

# Output:
🔍 Comparing competitor: https://www.rapidtables.com/tools/notepad.html
🏠 Against your site: https://appoftheday.com/notepad/

📋 Analysis Results:

✅ Your Advantages:
  • Your title length is optimally sized (50-60 chars)
  • You have fewer technical SEO issues

⚠️ Areas for Improvement:  
  • Competitor has more comprehensive content
  • Low density for important keyword: notepad

💡 Top Recommendations:
  1. [High] Content Depth: Add approximately 347 more words of valuable content
  2. [Medium] Keyword Optimization: Increase mentions of "notepad" by 3 occurrences
  3. [High] Technical SEO: Fix missing alt text on 2 images
```

### 3. Web Dashboard Features

#### 📁 Upload & Analyze CSV Data
- Drag & drop Ahrefs CSV exports
- Instant keyword analysis and visualization
- Position distribution charts
- Volume vs traffic correlation

#### 🔍 Competitor Analysis
- Enter competitor and your URLs
- Comprehensive side-by-side comparison
- Technical SEO gap analysis
- Content depth comparison

#### 📈 Keyword Gap Analysis
- High volume opportunities (volume >1000, position >10)
- Quick wins (position 11-20, volume >500)
- Low competition keywords
- Interactive visualizations

#### 📋 Reports & Export
- JSON export of all analysis data
- Comparison reports
- Keyword gap analysis reports

## 🔧 CSV Data Format

Your Ahrefs CSV should contain these columns:
```
Keyword, Volume, Organic traffic, Paid traffic, Average position, Locations, Location, Country, Organic clicks, Paid clicks
```

Example:
```csv
notepad,424550,58525,0,2.20,10,US,United States,600,96
online notepad free,1270,197,0,2.20,10,US,United States,600,96
text editor online,890,145,0,8.30,5,US,United States,120,0
```

## 🏗️ Architecture

```
Frontend (Streamlit Dashboard)
├── 📁 Upload Keywords (CSV Processor)
├── 🔍 Competitor Analysis (Website Analyzer)
├── 📈 Keyword Gaps (Opportunity Finder)
└── 📋 Reports (Export Manager)

Backend (Python Core)
├── keyword_analyzer.py (CSV Processing)
├── competitor_analyzer.py (Site Comparison)
├── pyseoanalyzer/ (Original SEO Engine)
└── main.py (CLI Interface)
```

## 🐳 Docker Deployment

### Basic Deployment
```bash
# Build image
docker build -t seo-analyzer .

# Run dashboard
docker run -p 8501:8501 seo-analyzer

# Run with data volume
docker run -v $(pwd)/data:/app/data -p 8501:8501 seo-analyzer
```

### Production Deployment
```yaml
# docker-compose.yml
version: '3.8'
services:
  seo-analyzer:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./reports:/app/reports
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

## 📊 Use Cases

### 1. **Keyword Research & Planning**
- Analyze competitor keyword strategies
- Find high-volume, low-competition opportunities
- Identify content gaps and quick wins

### 2. **Competitive Analysis**
- Technical SEO comparison
- Content depth analysis
- On-page optimization gaps

### 3. **Content Strategy**
- Keyword density optimization
- Content length recommendations
- Topic cluster identification

### 4. **SEO Auditing**
- Multi-site technical analysis
- Performance benchmarking
- Improvement prioritization

## 🤝 Contributing

This is a fork of [sethblack/python-seo-analyzer](https://github.com/sethblack/python-seo-analyzer) with additional features. 

To contribute:
1. Fork this repository
2. Create your feature branch
3. Follow existing code style
4. Add tests for new features
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Seth Black** - Original [python-seo-analyzer](https://github.com/sethblack/python-seo-analyzer)
- **Ahrefs** - Keyword data source and inspiration
- **Streamlit** - Beautiful dashboard framework

---

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/leadangle/python-seo-analyzer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/leadangle/python-seo-analyzer/discussions)
- 📧 **Email**: Contact via GitHub profile

**Made with ❤️ for the SEO community** 