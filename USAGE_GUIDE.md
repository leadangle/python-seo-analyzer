# 📖 SEO Competitor Analyzer - Usage Guide

Complete guide for using the enhanced SEO competitor analysis tool with your Ahrefs data.

## 🚀 Quick Start

### 1. Setup & Installation
```bash
# Clone the repository
git clone https://github.com/leadangle/python-seo-analyzer.git
cd python-seo-analyzer

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
python main.py dashboard
```

### 2. Using Your Ahrefs Data

#### Export from Ahrefs:
1. Go to your competitor's domain in Ahrefs
2. Navigate to **Organic Keywords** section
3. Click **Export** → **CSV**
4. Save the file (e.g., `competitor-keywords.csv`)

#### Expected CSV Format:
```csv
Keyword,Volume,Organic traffic,Paid traffic,Average position,Locations,Location,Country,Organic clicks,Paid clicks
notepad,424550,58525,0,2.20,10,US,United States,600,96
online notepad,201890,49993,0,2.50,10,US,United States,500,0
```

## 🎯 Analysis Workflows

### Workflow 1: Keyword Analysis Only
```bash
# Analyze your CSV data
python main.py keyword-analysis competitor-keywords.csv --output keyword-report.json

# View results
cat keyword-report.json | jq '.summary_stats'
```

**Output Example:**
```json
{
  "total_keywords": 2436,
  "total_volume": 4012300,
  "total_traffic": 183011,
  "avg_position": 48.0,
  "page_1_positions": 367
}
```

### Workflow 2: Competitor vs Your Site
```bash
# Full comparison with keyword insights
python main.py compare \
  https://www.rapidtables.com/tools/notepad.html \
  https://yoursite.com/notepad/ \
  --csv competitor-keywords.csv \
  --output comparison-report.json
```

**Key Insights Generated:**
- ✅ **Your Advantages**: Areas where you outperform
- ⚠️ **Improvement Areas**: Where competitor is stronger  
- 💡 **Recommendations**: Actionable SEO improvements
- 📊 **Technical Comparison**: Meta tags, content depth, etc.

### Workflow 3: Web Dashboard (Recommended)
```bash
# Launch interactive dashboard
python main.py dashboard
```

**Dashboard Features:**
1. **📁 Upload CSV**: Drag & drop Ahrefs exports
2. **🔍 Competitor Analysis**: Enter URLs for comparison
3. **📈 Keyword Gaps**: Visual opportunity analysis
4. **📋 Reports**: Export findings as JSON

## 📊 Understanding the Results

### Keyword Gap Analysis

#### High Volume Opportunities
Keywords with **volume >1000** and **position >10**:
```json
{
  "keyword": "online notepad",
  "volume": 201890,
  "current_position": 15.2,
  "traffic_potential": 49993
}
```
**Action**: Create dedicated content targeting these keywords.

#### Quick Wins  
Keywords ranking **position 11-20** with **volume >500**:
```json
{
  "keyword": "text editor online", 
  "volume": 12700,
  "current_position": 12.5,
  "potential_traffic_gain": 3940
}
```
**Action**: Optimize existing pages to move to page 1.

#### Low Competition Keywords
Keywords with **volume >100** and **position >20**:
```json
{
  "keyword": "simple notepad app",
  "volume": 890,
  "position": 25.3
}
```
**Action**: Create new content with minimal competition.

### Competitor Comparison Insights

#### Technical SEO Comparison
```json
{
  "title_comparison": {
    "competitor_title_length": 45,
    "my_title_length": 28,
    "recommendation": "Expand title to 50-60 characters"
  },
  "content_analysis": {
    "word_count_gap": 347,
    "recommendation": "Add more comprehensive content"
  }
}
```

#### Content Gaps
```json
{
  "keyword_density_comparison": {
    "keyword": "notepad",
    "competitor_density": 8,
    "my_density": 3,
    "gap": 5,
    "recommendation": "Increase keyword mentions by 5"
  }
}
```

## 🎨 Dashboard Usage

### 1. Upload & Analyze Keywords
1. Go to **📁 Upload Keywords** page
2. Upload your Ahrefs CSV file
3. Review the **Data Preview** and **Summary Statistics**
4. Navigate to **📊 Dashboard** to see visualizations

### 2. Competitor Analysis
1. Go to **🔍 Competitor Analysis** page  
2. Enter competitor URL (e.g., `https://competitor.com/page`)
3. Enter your URL (e.g., `https://yoursite.com/page`)
4. Click **🚀 Start Analysis**
5. Review results and recommendations

### 3. Keyword Gap Analysis
1. Go to **📈 Keyword Gaps** page
2. View **High Volume Opportunities** table
3. Analyze **Quick Wins** for immediate improvements
4. Export findings using **📋 Reports** page

## 🐳 Docker Deployment

### Local Development
```bash
# Build and run
docker build -t seo-analyzer .
docker run -p 8501:8501 seo-analyzer

# With data persistence
docker run -v $(pwd)/data:/app/data -p 8501:8501 seo-analyzer
```

### Production Deployment
```bash
# Using docker-compose
docker-compose up -d

# With environment variables
ANTHROPIC_API_KEY=your_key docker-compose up -d
```

**Access**: http://localhost:8501

### SFTP Deployment (Your Use Case)
```bash
# Build image
docker build -t seo-analyzer .
docker save seo-analyzer | gzip > seo-analyzer.tar.gz

# Upload to server via SFTP
scp seo-analyzer.tar.gz user@yourserver.com:/path/

# On server:
docker load < seo-analyzer.tar.gz
docker run -d -p 8501:8501 --name seo-analyzer seo-analyzer
```

## 🔧 Advanced Usage

### Custom Analysis Scripts
```python
from keyword_analyzer import CSVKeywordAnalyzer
from competitor_analyzer import CompetitorAnalyzer

# Load your data
analyzer = CSVKeywordAnalyzer('your-data.csv')
analyzer.load_csv_data()

# Get insights
stats = analyzer.get_summary_stats()
top_keywords = analyzer.get_top_keywords(50)
gaps = analyzer.get_keyword_gaps('competitor.com', 'yoursite.com')

# Competitor analysis
comp_analyzer = CompetitorAnalyzer(analyzer)
results = comp_analyzer.analyze_competitor_vs_my_site(
    'https://competitor.com', 
    'https://yoursite.com'
)
```

### Batch Analysis
```bash
# Analyze multiple competitors
for competitor in competitor1.csv competitor2.csv competitor3.csv; do
  python main.py keyword-analysis $competitor --output ${competitor%.csv}-report.json
done

# Compare against multiple competitors
python main.py compare https://competitor1.com https://yoursite.com --csv competitor1.csv
python main.py compare https://competitor2.com https://yoursite.com --csv competitor2.csv
```

## 📈 Optimization Workflow

### 1. Initial Analysis
- Upload Ahrefs CSV data
- Run competitor comparison
- Identify top opportunities

### 2. Content Strategy
- Target **High Volume Opportunities** with new content
- Optimize existing pages for **Quick Wins**
- Create content for **Low Competition Keywords**

### 3. Technical Optimization
- Fix SEO issues identified in comparison
- Optimize title tags and meta descriptions
- Improve content depth and keyword density

### 4. Monitoring
- Re-run analysis monthly
- Track position improvements
- Adjust strategy based on new opportunities

## 🚨 Troubleshooting

### Common Issues

#### CSV Upload Errors
```
Error: Missing columns: ['Location', 'Country']
```
**Solution**: The tool handles missing columns automatically. This warning is normal.

#### Analysis Timeout
```
Error: Analysis timeout after 60 seconds
```
**Solution**: Large sites may take longer. Use the CLI for heavy analysis:
```bash
python main.py analyze https://large-site.com --follow-links=false
```

#### Memory Issues
```
Error: Out of memory processing large CSV
```
**Solution**: Process in chunks or use a subset:
```bash
head -1000 large-file.csv > subset.csv
python main.py keyword-analysis subset.csv
```

### Performance Tips
- Use `--follow-links=false` for faster analysis
- Process CSV files under 10MB for best performance
- Run Docker with increased memory: `docker run -m 2g`

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/leadangle/python-seo-analyzer/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/leadangle/python-seo-analyzer/discussions)
- 📧 **Contact**: Via GitHub profile

---

**Happy SEO analyzing! 🚀** 