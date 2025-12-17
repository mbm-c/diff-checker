import streamlit as st
import difflib
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
    
    diff = difflib.HtmlDiff(wrapcolumn=80)
    html_diff = diff.make_file(
        lines1,
        lines2,
        fromdesc='Text 1',
        todesc='Text 2',
        context=True,
        numlines=3
    )
    
    return html_diff


def main():
    st.set_page_config(
        page_title="Diff Checker",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Diff Checker")
    st.markdown("Compare two texts and see the differences between them.")
    
    # Create two columns for side-by-side input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Text 1")
        text1 = st.text_area(
            "Enter first text:",
            height=300,
            key="text1",
            placeholder="Enter your first text here..."
        )
    
    with col2:
        st.subheader("Text 2")
        text2 = st.text_area(
            "Enter second text:",
            height=300,
            key="text2",
            placeholder="Enter your second text here..."
        )
    
    # Options
    st.divider()
    ignore_whitespace = st.checkbox(
        "Ignore leading whitespace/tabs",
        value=False,
        help="When enabled, leading spaces and tabs at the beginning of each line will be ignored during comparison. Useful for comparing code with different indentation."
    )
    
    # Compare button
    if st.button("Compare", type="primary", use_container_width=True):
        if not text1 and not text2:
            st.warning("Please enter text in at least one field to compare.")
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
                st.success("✅ Texts are identical!" + (" (ignoring leading whitespace)" if ignore_whitespace else ""))
            else:
                # Show diff options
                tab1, tab2 = st.tabs(["Unified Diff", "Side-by-Side HTML Diff"])
                
                with tab1:
                    st.subheader("Unified Diff Output")
                    diff_output = generate_diff(text1, text2, ignore_leading_whitespace=ignore_whitespace)
                    if diff_output:
                        st.code(diff_output, language="diff")
                    else:
                        st.info("No differences found.")
                
                with tab2:
                    st.subheader("Side-by-Side HTML Diff")
                    html_diff = generate_html_diff(text1, text2, ignore_leading_whitespace=ignore_whitespace)
                    st.components.v1.html(html_diff, height=600, scrolling=True)
                
                # Show statistics
                with st.expander("📊 Diff Statistics"):
                    lines1 = text1.splitlines()
                    lines2 = text2.splitlines()
                    
                    if ignore_whitespace:
                        lines1_compare = [line.lstrip(' \t') for line in lines1]
                        lines2_compare = [line.lstrip(' \t') for line in lines2]
                    else:
                        lines1_compare = lines1
                        lines2_compare = lines2
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    
                    with col_stat1:
                        st.metric("Lines in Text 1", len(lines1))
                    with col_stat2:
                        st.metric("Lines in Text 2", len(lines2))
                    with col_stat3:
                        # Count differences
                        diff_lines = list(difflib.unified_diff(
                            lines1_compare,
                            lines2_compare,
                            lineterm='',
                            n=0
                        ))
                        diff_count = len([line for line in diff_lines if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))])
                        st.metric("Differences", diff_count)


if __name__ == "__main__":
    main()
