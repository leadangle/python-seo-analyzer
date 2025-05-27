import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import logging
from typing import Dict, List
import tempfile

# Import our custom modules
from keyword_analyzer import CSVKeywordAnalyzer
from competitor_analyzer import CompetitorAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="SEO Competitor Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class SEODashboard:
    def __init__(self):
        self.keyword_analyzer = None
        self.competitor_analyzer = None
    
    def run(self):
        """Main dashboard function"""
        
        # Header
        st.markdown('<h1 class="main-header">🔍 SEO Competitor Analyzer</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Sidebar for navigation
        with st.sidebar:
            st.image("https://via.placeholder.com/200x100/1f77b4/white?text=SEO+Tool", width=200)
            st.title("Navigation")
            
            page = st.selectbox(
                "Choose Analysis Type",
                ["📊 Dashboard", "📁 Upload Keywords", "🔍 Competitor Analysis", "📈 Keyword Gaps", "📋 Reports"]
            )
        
        # Main content based on selected page
        if page == "📊 Dashboard":
            self.show_dashboard()
        elif page == "📁 Upload Keywords":
            self.show_upload_page()
        elif page == "🔍 Competitor Analysis":
            self.show_competitor_analysis()
        elif page == "📈 Keyword Gaps":
            self.show_keyword_gaps()
        elif page == "📋 Reports":
            self.show_reports()
    
    def show_dashboard(self):
        """Show main dashboard with overview"""
        
        st.header("📊 SEO Analysis Dashboard")
        
        # Check if data is loaded
        if 'keyword_data' not in st.session_state:
            st.warning("⚠️ Please upload your Ahrefs CSV data first using the 'Upload Keywords' page.")
            return
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        stats = st.session_state.get('keyword_stats', {})
        
        with col1:
            st.metric(
                label="Total Keywords",
                value=stats.get('total_keywords', 0),
                delta=f"Avg Position: {stats.get('avg_position', 0):.1f}"
            )
        
        with col2:
            st.metric(
                label="Total Search Volume",
                value=f"{stats.get('total_volume', 0):,}",
                delta=f"Avg Volume: {stats.get('avg_volume', 0):.0f}"
            )
        
        with col3:
            st.metric(
                label="Total Organic Traffic",
                value=f"{stats.get('total_traffic', 0):,}",
                delta=f"Page 1 Keywords: {stats.get('page_1_positions', 0)}"
            )
        
        with col4:
            st.metric(
                label="Top 10 Rankings",
                value=stats.get('top_10_positions', 0),
                delta=f"Page 2: {stats.get('page_2_positions', 0)}"
            )
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_position_distribution()
        
        with col2:
            self.show_volume_vs_traffic()
        
        # Top keywords table
        st.subheader("🏆 Top Keywords by Volume")
        self.show_top_keywords_table()
    
    def show_upload_page(self):
        """Show CSV upload page"""
        
        st.header("📁 Upload Ahrefs Keyword Data")
        st.markdown("Upload your Ahrefs CSV export to begin the analysis.")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="Export your keyword data from Ahrefs as a CSV file"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process the CSV
                with st.spinner("Processing CSV data..."):
                    analyzer = CSVKeywordAnalyzer(tmp_path)
                    success = analyzer.load_csv_data()
                
                if success:
                    st.success("✅ CSV data loaded successfully!")
                    
                    # Store in session state
                    st.session_state['keyword_analyzer'] = analyzer
                    st.session_state['keyword_data'] = analyzer.keywords_data
                    st.session_state['keyword_stats'] = analyzer.get_summary_stats()
                    
                    # Show preview
                    st.subheader("📋 Data Preview")
                    preview_data = []
                    for kw in analyzer.keywords_data[:10]:
                        preview_data.append({
                            'Keyword': kw.keyword,
                            'Volume': kw.volume,
                            'Traffic': kw.organic_traffic,
                            'Position': kw.average_position,
                            'Country': kw.country
                        })
                    
                    df = pd.DataFrame(preview_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Summary stats
                    stats = analyzer.get_summary_stats()
                    st.subheader("📊 Summary Statistics")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Keywords", stats['total_keywords'])
                        st.metric("Total Volume", f"{stats['total_volume']:,}")
                    with col2:
                        st.metric("Total Traffic", f"{stats['total_traffic']:,}")
                        st.metric("Average Position", f"{stats['avg_position']:.1f}")
                    with col3:
                        st.metric("Page 1 Rankings", stats['page_1_positions'])
                        st.metric("Page 2 Rankings", stats['page_2_positions'])
                
                else:
                    st.error("❌ Error processing CSV file. Please check the format.")
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    def show_competitor_analysis(self):
        """Show competitor analysis page"""
        
        st.header("🔍 Competitor vs Your Site Analysis")
        
        if 'keyword_analyzer' not in st.session_state:
            st.warning("⚠️ Please upload your keyword data first.")
            return
        
        # Input URLs
        col1, col2 = st.columns(2)
        
        with col1:
            competitor_url = st.text_input(
                "🏢 Competitor URL",
                placeholder="https://www.rapidtables.com/tools/notepad.html",
                help="Enter the competitor page URL to analyze"
            )
        
        with col2:
            my_url = st.text_input(
                "🏠 Your URL",
                placeholder="https://appoftheday.com/notepad/",
                help="Enter your page URL to compare"
            )
        
        if st.button("🚀 Start Analysis", type="primary"):
            if competitor_url and my_url:
                try:
                    with st.spinner("Analyzing both websites... This may take a few minutes."):
                        # Initialize competitor analyzer
                        keyword_analyzer = st.session_state['keyword_analyzer']
                        comp_analyzer = CompetitorAnalyzer(keyword_analyzer)
                        
                        # Perform analysis
                        results = comp_analyzer.analyze_competitor_vs_my_site(competitor_url, my_url)
                        
                        # Store results
                        st.session_state['comparison_results'] = results
                    
                    st.success("✅ Analysis completed!")
                    
                    # Display results
                    self.display_comparison_results(results)
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
            else:
                st.error("❌ Please enter both URLs")
    
    def show_keyword_gaps(self):
        """Show keyword gap analysis"""
        
        st.header("📈 Keyword Gap Analysis")
        
        if 'keyword_analyzer' not in st.session_state:
            st.warning("⚠️ Please upload your keyword data first.")
            return
        
        keyword_analyzer = st.session_state['keyword_analyzer']
        
        # Get keyword gaps
        gaps = keyword_analyzer.get_keyword_gaps("", "")
        
        # High volume opportunities
        st.subheader("🎯 High Volume Opportunities")
        if gaps['high_volume_opportunities']:
            df_high_vol = pd.DataFrame(gaps['high_volume_opportunities'])
            st.dataframe(df_high_vol, use_container_width=True)
            
            # Visualization
            fig = px.scatter(
                df_high_vol,
                x='current_position',
                y='volume',
                size='traffic_potential',
                hover_data=['keyword'],
                title="High Volume Keywords vs Current Position",
                labels={'current_position': 'Current Position', 'volume': 'Search Volume'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No high volume opportunities found in the current data.")
        
        # Quick wins
        st.subheader("⚡ Quick Wins (Page 2 Rankings)")
        if gaps['position_improvement_targets']:
            df_quick_wins = pd.DataFrame(gaps['position_improvement_targets'])
            st.dataframe(df_quick_wins, use_container_width=True)
        else:
            st.info("No quick win opportunities found.")
        
        # Low competition keywords
        st.subheader("🎯 Low Competition Keywords")
        if gaps['low_competition_keywords']:
            df_low_comp = pd.DataFrame(gaps['low_competition_keywords'])
            st.dataframe(df_low_comp, use_container_width=True)
        else:
            st.info("No low competition keywords found.")
    
    def show_reports(self):
        """Show reports and export options"""
        
        st.header("📋 Reports & Export")
        
        if 'keyword_analyzer' not in st.session_state:
            st.warning("⚠️ Please upload your keyword data first.")
            return
        
        keyword_analyzer = st.session_state['keyword_analyzer']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Keyword Analysis Report")
            if st.button("Generate Keyword Report"):
                # Generate report
                report_data = {
                    'summary_stats': keyword_analyzer.get_summary_stats(),
                    'top_keywords': [
                        {
                            'keyword': kw.keyword,
                            'volume': kw.volume,
                            'traffic': kw.organic_traffic,
                            'position': kw.average_position
                        } for kw in keyword_analyzer.get_top_keywords(50)
                    ],
                    'keyword_gaps': keyword_analyzer.get_keyword_gaps("", "")
                }
                
                # Convert to JSON for download
                report_json = json.dumps(report_data, indent=2)
                st.download_button(
                    label="⬇️ Download JSON Report",
                    data=report_json,
                    file_name="keyword_analysis_report.json",
                    mime="application/json"
                )
        
        with col2:
            st.subheader("🔍 Competitor Analysis Report")
            if 'comparison_results' in st.session_state:
                if st.button("Generate Competitor Report"):
                    results = st.session_state['comparison_results']
                    report_json = json.dumps(results, indent=2, default=str)
                    st.download_button(
                        label="⬇️ Download Comparison Report",
                        data=report_json,
                        file_name="competitor_analysis_report.json",
                        mime="application/json"
                    )
            else:
                st.info("No competitor analysis data available. Run a comparison first.")
    
    def display_comparison_results(self, results: Dict):
        """Display competitor analysis results"""
        
        if 'error' in results:
            st.error(f"❌ Analysis error: {results['error']}")
            return
        
        # Summary
        st.subheader("📋 Analysis Summary")
        
        comparison = results.get('comparison', {})
        advantages = comparison.get('advantages', [])
        disadvantages = comparison.get('disadvantages', [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Your Advantages")
            if advantages:
                for advantage in advantages:
                    st.markdown(f"• {advantage}")
            else:
                st.info("No clear advantages identified")
        
        with col2:
            st.markdown("#### ⚠️ Areas for Improvement")
            if disadvantages:
                for disadvantage in disadvantages:
                    st.markdown(f"• {disadvantage}")
            else:
                st.success("No significant disadvantages found!")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = results.get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                with st.expander(f"{i}. {rec['category']} - {rec['priority']} Priority"):
                    st.markdown(f"**Issue:** {rec['issue']}")
                    st.markdown(f"**Recommendation:** {rec['recommendation']}")
                    st.markdown(f"**Impact:** {rec['impact']}")
        else:
            st.info("No specific recommendations generated.")
        
        # Detailed comparison
        with st.expander("📊 Detailed Technical Comparison"):
            st.json(comparison)
    
    def show_position_distribution(self):
        """Show position distribution chart"""
        
        if 'keyword_data' not in st.session_state:
            return
        
        keyword_data = st.session_state['keyword_data']
        positions = [kw.average_position for kw in keyword_data if kw.average_position > 0]
        
        if not positions:
            st.info("No position data available")
            return
        
        # Create position ranges
        position_ranges = {
            '1-3': len([p for p in positions if 1 <= p <= 3]),
            '4-10': len([p for p in positions if 4 <= p <= 10]),
            '11-20': len([p for p in positions if 11 <= p <= 20]),
            '21-50': len([p for p in positions if 21 <= p <= 50]),
            '50+': len([p for p in positions if p > 50])
        }
        
        fig = px.pie(
            values=list(position_ranges.values()),
            names=list(position_ranges.keys()),
            title="Position Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def show_volume_vs_traffic(self):
        """Show volume vs traffic scatter plot"""
        
        if 'keyword_data' not in st.session_state:
            return
        
        keyword_data = st.session_state['keyword_data']
        
        # Prepare data for top 100 keywords by volume
        top_keywords = sorted(keyword_data, key=lambda x: x.volume, reverse=True)[:100]
        
        df = pd.DataFrame([
            {
                'keyword': kw.keyword,
                'volume': kw.volume,
                'traffic': kw.organic_traffic,
                'position': kw.average_position
            } for kw in top_keywords
        ])
        
        fig = px.scatter(
            df,
            x='volume',
            y='traffic',
            color='position',
            hover_data=['keyword'],
            title="Search Volume vs Organic Traffic",
            labels={'volume': 'Search Volume', 'traffic': 'Organic Traffic'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def show_top_keywords_table(self):
        """Show top keywords table"""
        
        if 'keyword_analyzer' not in st.session_state:
            return
        
        keyword_analyzer = st.session_state['keyword_analyzer']
        top_keywords = keyword_analyzer.get_top_keywords(20)
        
        # Create DataFrame
        df = pd.DataFrame([
            {
                'Keyword': kw.keyword,
                'Volume': f"{kw.volume:,}",
                'Traffic': f"{kw.organic_traffic:,}",
                'Position': f"{kw.average_position:.1f}",
                'Country': kw.country
            } for kw in top_keywords
        ])
        
        st.dataframe(df, use_container_width=True)

# Main execution
if __name__ == "__main__":
    dashboard = SEODashboard()
    dashboard.run() 