#!/usr/bin/env python3
"""
SEO Competitor Analyzer - Enhanced Python SEO Analysis Tool
Based on sethblack/python-seo-analyzer with competitor analysis features
"""

import argparse
import sys
import os
import subprocess
from pathlib import Path

def run_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Starting SEO Competitor Analyzer Dashboard...")
    print("📊 Dashboard will open in your browser at http://localhost:8501")
    
    dashboard_path = Path(__file__).parent / "dashboard.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(dashboard_path), "--server.port=8501"]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting dashboard: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")

def run_keyword_analysis(csv_file, output=None):
    """Run keyword analysis on CSV file"""
    print(f"📁 Analyzing keyword data from: {csv_file}")
    
    from keyword_analyzer import CSVKeywordAnalyzer
    
    try:
        # Load and analyze CSV
        analyzer = CSVKeywordAnalyzer(csv_file)
        success = analyzer.load_csv_data()
        
        if not success:
            print("❌ Failed to load CSV data")
            return False
        
        # Print summary stats
        stats = analyzer.get_summary_stats()
        print("\n📊 Summary Statistics:")
        print(f"  Total Keywords: {stats['total_keywords']}")
        print(f"  Total Volume: {stats['total_volume']:,}")
        print(f"  Total Traffic: {stats['total_traffic']:,}")
        print(f"  Average Position: {stats['avg_position']:.1f}")
        print(f"  Page 1 Rankings: {stats['page_1_positions']}")
        
        # Show top keywords
        print("\n🏆 Top 10 Keywords by Volume:")
        top_keywords = analyzer.get_top_keywords(10)
        for i, kw in enumerate(top_keywords, 1):
            print(f"  {i:2}. {kw.keyword:<30} | Volume: {kw.volume:>8,} | Traffic: {kw.organic_traffic:>8,} | Pos: {kw.average_position:>5.1f}")
        
        # Export if requested
        if output:
            success = analyzer.export_analysis(output)
            if success:
                print(f"\n💾 Analysis exported to: {output}")
            else:
                print("\n❌ Failed to export analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def run_competitor_comparison(competitor_url, my_url, csv_file=None, output=None):
    """Run competitor vs my site comparison"""
    print(f"🔍 Comparing competitor: {competitor_url}")
    print(f"🏠 Against your site: {my_url}")
    
    from competitor_analyzer import CompetitorAnalyzer
    from keyword_analyzer import CSVKeywordAnalyzer
    
    try:
        # Load keyword data if provided
        keyword_analyzer = None
        if csv_file:
            print(f"📁 Loading keyword data from: {csv_file}")
            keyword_analyzer = CSVKeywordAnalyzer(csv_file)
            if not keyword_analyzer.load_csv_data():
                print("⚠️ Warning: Failed to load keyword data, continuing without it")
                keyword_analyzer = None
        
        # Run comparison
        comp_analyzer = CompetitorAnalyzer(keyword_analyzer)
        results = comp_analyzer.analyze_competitor_vs_my_site(competitor_url, my_url)
        
        if 'error' in results:
            print(f"❌ Analysis error: {results['error']}")
            return False
        
        # Display results
        print("\n📋 Analysis Results:")
        
        comparison = results.get('comparison', {})
        advantages = comparison.get('advantages', [])
        disadvantages = comparison.get('disadvantages', [])
        
        if advantages:
            print("\n✅ Your Advantages:")
            for advantage in advantages:
                print(f"  • {advantage}")
        
        if disadvantages:
            print("\n⚠️ Areas for Improvement:")
            for disadvantage in disadvantages:
                print(f"  • {disadvantage}")
        
        # Show recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print("\n💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
        
        # Export if requested
        if output:
            success = comp_analyzer.export_comparison_report(results, output)
            if success:
                print(f"\n💾 Comparison report exported to: {output}")
            else:
                print("\n❌ Failed to export comparison report")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        return False

def run_original_seo_analyzer(url, **kwargs):
    """Run the original SEO analyzer"""
    print(f"🔍 Running original SEO analysis on: {url}")
    
    from pyseoanalyzer import analyze
    
    try:
        # Run analysis with provided parameters
        results = analyze(url, **kwargs)
        
        # Display basic results
        if 'page' in results:
            page = results['page']
            print(f"\n📄 Page Analysis:")
            print(f"  Title: {page.get('title', 'N/A')}")
            print(f"  Description: {page.get('description', 'N/A')[:100]}...")
            print(f"  H1 Tags: {len(page.get('h1', []))}")
            print(f"  H2 Tags: {len(page.get('h2', []))}")
        
        if 'words' in results:
            words = results['words']
            print(f"\n📝 Content Analysis:")
            print(f"  Word Count: {words.get('count', 0)}")
            print(f"  Unique Words: {len(words.get('keywords', {}))}")
        
        if 'warnings' in results:
            warnings = results['warnings']
            if warnings:
                print(f"\n⚠️ SEO Issues ({len(warnings)}):")
                for warning in warnings[:5]:
                    print(f"  • {warning}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SEO Competitor Analyzer - Enhanced Python SEO Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch web dashboard
  python main.py dashboard
  
  # Analyze keywords from CSV
  python main.py keyword-analysis data.csv --output report.json
  
  # Compare competitor vs your site
  python main.py compare https://competitor.com https://mysite.com --csv data.csv
  
  # Run original SEO analyzer
  python main.py analyze https://example.com --sitemap sitemap.xml
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch web dashboard')
    
    # Keyword analysis command
    keyword_parser = subparsers.add_parser('keyword-analysis', help='Analyze keywords from CSV')
    keyword_parser.add_argument('csv_file', help='Path to Ahrefs CSV file')
    keyword_parser.add_argument('--output', '-o', help='Output JSON file for analysis results')
    
    # Competitor comparison command
    compare_parser = subparsers.add_parser('compare', help='Compare competitor vs your site')
    compare_parser.add_argument('competitor_url', help='Competitor website URL')
    compare_parser.add_argument('my_url', help='Your website URL')
    compare_parser.add_argument('--csv', help='Optional: Ahrefs CSV file for keyword insights')
    compare_parser.add_argument('--output', '-o', help='Output JSON file for comparison results')
    
    # Original analyzer command
    analyze_parser = subparsers.add_parser('analyze', help='Run original SEO analyzer')
    analyze_parser.add_argument('url', help='Website URL to analyze')
    analyze_parser.add_argument('--sitemap', help='Path to sitemap.xml')
    analyze_parser.add_argument('--follow-links', action='store_true', help='Follow internal links')
    analyze_parser.add_argument('--analyze-headings', action='store_true', help='Analyze heading tags')
    analyze_parser.add_argument('--analyze-extra-tags', action='store_true', help='Analyze extra tags')
    analyze_parser.add_argument('--output-format', choices=['json', 'html'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    success = False
    
    if args.command == 'dashboard':
        run_dashboard()
        
    elif args.command == 'keyword-analysis':
        success = run_keyword_analysis(args.csv_file, args.output)
        
    elif args.command == 'compare':
        success = run_competitor_comparison(args.competitor_url, args.my_url, args.csv, args.output)
        
    elif args.command == 'analyze':
        kwargs = {
            'sitemap': args.sitemap,
            'follow_links': args.follow_links,
            'analyze_headings': args.analyze_headings,
            'analyze_extra_tags': args.analyze_extra_tags
        }
        # Remove None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        success = run_original_seo_analyzer(args.url, **kwargs)
    
    if args.command != 'dashboard':
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 