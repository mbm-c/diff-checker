import streamlit as st
import difflib
import re
from typing import List


def strip_leading_whitespace(lines: List[str]) -> List[str]:
    """
    Strip leading whitespace (spaces and tabs) from each line.
    
    Args:
        lines: List of lines to process
        
    Returns:
        List of lines with leading whitespace removed
    """
    return [line.lstrip(' \t') + '\n' if line.endswith('\n') else line.lstrip(' \t') 
            for line in lines]


def generate_diff(text1: str, text2: str, ignore_leading_whitespace: bool = False) -> str:
    """
    Generate a unified diff between two texts.
    
    Args:
        text1: First text input
        text2: Second text input
        ignore_leading_whitespace: If True, strip leading whitespace before comparing
        
    Returns:
        Unified diff string
    """
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    
    if ignore_leading_whitespace:
        lines1 = strip_leading_whitespace(lines1)
        lines2 = strip_leading_whitespace(lines2)
    
    diff = difflib.unified_diff(
        lines1,
        lines2,
        fromfile='Text 1',
        tofile='Text 2',
        lineterm='',
        n=3
    )
    
    return '\n'.join(diff)


def generate_html_diff(text1: str, text2: str, ignore_leading_whitespace: bool = False) -> str:
    """
    Generate an HTML formatted diff with color coding.
    
    Args:
        text1: First text input
        text2: Second text input
        ignore_leading_whitespace: If True, strip leading whitespace before comparing
        
    Returns:
        HTML formatted diff string
    """
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    if ignore_leading_whitespace:
        lines1 = [line.lstrip(' \t') for line in lines1]
        lines2 = [line.lstrip(' \t') for line in lines2]
    
    diff = difflib.HtmlDiff(wrapcolumn=80, tabsize=4)
    html_diff = diff.make_file(
        lines1,
        lines2,
        fromdesc='Text 1',
        todesc='Text 2',
        context=True,
        numlines=3
    )
    
    # Extract the table and styles from the complete HTML document
    # difflib.HtmlDiff.make_file() returns a complete HTML document
    
    # Extract style block
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html_diff, re.DOTALL)
    styles = style_match.group(0) if style_match else ''
    
    # Extract table content
    table_match = re.search(r'<table[^>]*>(.*?)</table>', html_diff, re.DOTALL)
    table_content = table_match.group(0) if table_match else html_diff
    
    # Return a complete HTML document with proper structure
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {styles}
        <style>
            body {{
                margin: 0;
                padding: 10px;
                font-family: monospace;
                background-color: #ffffff;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .diff_add {{
                background-color: #d4edda;
            }}
            .diff_chg {{
                background-color: #fff3cd;
            }}
            .diff_sub {{
                background-color: #f8d7da;
            }}
        </style>
    </head>
    <body>
        <div style="width: 100%; overflow-x: auto;">
            {table_content}
        </div>
    </body>
    </html>
    """


def main():
    st.set_page_config(
        page_title="Diff Checker",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stTextArea > div > div > textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 14px;
        line-height: 1.6;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-left: 5px solid #10b981;
    }
    .warning-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        border-left: 5px solid #f59e0b;
    }
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .input-section:hover {
        border-color: #667eea;
        transition: all 0.3s ease;
    }
    h3 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Diff Checker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare two texts and visualize the differences between them</p>', unsafe_allow_html=True)
    
    # Privacy notice
    with st.expander("🔒 Privacy & Security", expanded=False):
        st.markdown("""
        **Your data is completely private and secure:**
        
        - ✅ **No logging**: We do not log, store, or track any content you enter
        - ✅ **No data collection**: Your inputs are processed in memory only and never stored
        - ✅ **No external requests**: Your data is never sent to third-party services
        - ✅ **No persistence**: Your data is never saved to files or databases
        - ✅ **In-memory processing**: All diff calculations happen in server memory and are discarded after processing
        
        This application processes your text in memory on the server. Your data is only kept temporarily 
        during the comparison and is immediately discarded. We have no way to see, access, or store 
        your content after the session ends.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create two columns for side-by-side input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 📝 Text 1")
        text1 = st.text_area(
            "Enter first text:",
            height=350,
            key="text1",
            placeholder="Enter your first text here...\n\nExample:\ndef hello():\n    print('Hello, World!')",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 📝 Text 2")
        text2 = st.text_area(
            "Enter second text:",
            height=350,
            key="text2",
            placeholder="Enter your second text here...\n\nExample:\ndef hello():\n    print('Hello, World!')",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Options section
    col_options1, col_options2, col_options3 = st.columns([1, 2, 1])
    with col_options2:
        ignore_whitespace = st.checkbox(
            "⚙️ Ignore leading whitespace/tabs",
            value=False,
            help="When enabled, leading spaces and tabs at the beginning of each line will be ignored during comparison. Useful for comparing code with different indentation."
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Compare button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        compare_clicked = st.button("🚀 Compare Texts", type="primary", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if compare_clicked:
        if not text1 and not text2:
            st.markdown("""
            <div class="warning-box">
                <h4>⚠️ No Input Provided</h4>
                <p>Please enter text in at least one field to compare.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Prepare texts for comparison
            text1_compare = text1
            text2_compare = text2
            
            if ignore_whitespace:
                # Strip leading whitespace for comparison
                lines1_stripped = [line.lstrip(' \t') for line in text1.splitlines()]
                lines2_stripped = [line.lstrip(' \t') for line in text2.splitlines()]
                text1_compare = '\n'.join(lines1_stripped)
                text2_compare = '\n'.join(lines2_stripped)
            
            if text1_compare == text2_compare:
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Texts are Identical!</h3>
                    <p>{'Leading whitespace differences were ignored.' if ignore_whitespace else 'Both texts match exactly.'}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Show statistics first
                lines1 = text1.splitlines()
                lines2 = text2.splitlines()
                
                if ignore_whitespace:
                    lines1_compare = [line.lstrip(' \t') for line in lines1]
                    lines2_compare = [line.lstrip(' \t') for line in lines2]
                else:
                    lines1_compare = lines1
                    lines2_compare = lines2
                
                # Count differences
                diff_lines = list(difflib.unified_diff(
                    lines1_compare,
                    lines2_compare,
                    lineterm='',
                    n=0
                ))
                diff_count = len([line for line in diff_lines if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))])
                
                # Statistics cards
                st.markdown("### 📊 Comparison Statistics")
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric(
                        label="📄 Lines in Text 1",
                        value=len(lines1),
                        delta=None
                    )
                with col_stat2:
                    st.metric(
                        label="📄 Lines in Text 2",
                        value=len(lines2),
                        delta=None
                    )
                with col_stat3:
                    st.metric(
                        label="🔀 Differences",
                        value=diff_count,
                        delta=None
                    )
                with col_stat4:
                    similarity = difflib.SequenceMatcher(None, text1_compare, text2_compare).ratio() * 100
                    st.metric(
                        label="📈 Similarity",
                        value=f"{similarity:.1f}%",
                        delta=None
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Show diff options
                tab1, tab2 = st.tabs(["📋 Unified Diff", "🎨 Side-by-Side HTML Diff"])
                
                with tab1:
                    st.markdown("### 📋 Unified Diff Output")
                    diff_output = generate_diff(text1, text2, ignore_leading_whitespace=ignore_whitespace)
                    if diff_output:
                        st.code(diff_output, language="diff")
                    else:
                        st.info("No differences found.")
                
                with tab2:
                    st.markdown("### 🎨 Side-by-Side HTML Diff")
                    html_diff = generate_html_diff(text1, text2, ignore_leading_whitespace=ignore_whitespace)
                    st.components.v1.html(html_diff, height=600, scrolling=True)


if __name__ == "__main__":
    main()
