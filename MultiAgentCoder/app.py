import os
import re
import streamlit as st
from groq import RateLimitError

from agents.workflow import Workflow


st.set_page_config(
    page_title="Multi-Agent Coding Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Coding Assistant")

st.markdown("""
Generate complete responsive HTML, CSS and JavaScript websites using multiple AI agents.
""")

prompt = st.text_area(
    "Describe your project",
    height=180,
    placeholder="Example: Build a Modern Responsive Calculator Website"
)

if st.button("🚀 Generate Project", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a project description.")
        st.stop()

    try:

        with st.spinner("🤖 AI Agents are building your project..."):

            workflow = Workflow()

            result = workflow.run(prompt)

        st.success("✅ Project Generated Successfully!")
        st.balloons()

        # -----------------------
        # Preview Button
        # -----------------------

        if isinstance(result, dict):

            preview_url = result.get("preview_url")

            if preview_url:
                st.link_button(
                    "🌐 Preview Website",
                    preview_url,
                    use_container_width=True
                )

            # -----------------------
            # Download ZIP
            # -----------------------

            zip_path = result.get("zip")

            if zip_path and os.path.exists(zip_path):

                with open(zip_path, "rb") as f:

                    st.download_button(
                        label="📥 Download Project ZIP",
                        data=f,
                        file_name=os.path.basename(zip_path),
                        mime="application/zip",
                        use_container_width=True
                    )

            # -----------------------
            # Generated Files
            # -----------------------

            folder = result.get("folder")

            if folder and os.path.isdir(folder):

                st.subheader("📁 Generated Files")

                files = os.listdir(folder)

                for file in files:
                    st.write("📄", file)

                st.code(folder)

        elif isinstance(result, str):

            if os.path.isdir(result):

                st.subheader("📁 Generated Files")

                files = os.listdir(result)

                for file in files:
                    st.write("📄", file)

                st.code(result)

            elif result.endswith(".zip") and os.path.exists(result):

                with open(result, "rb") as f:

                    st.download_button(
                        "📥 Download ZIP",
                        f,
                        file_name=os.path.basename(result),
                        mime="application/zip",
                        use_container_width=True
                    )

            else:
                st.error("Workflow returned an unknown result.")

        else:
            st.error("Invalid response returned from Workflow.")

    except RateLimitError as e:

        message = str(e)

        wait_time = "a few minutes"

        match = re.search(
            r"try again in ([0-9hms\.]+)",
            message,
            re.IGNORECASE
        )

        if match:
            wait_time = match.group(1)

        st.warning("⚠️ AI Usage Limit Reached")

        st.info(f"""
The AI service has temporarily reached its usage limit.

⏳ **Please try again after:** {wait_time}

No technical knowledge is required.

Simply wait for the timer to finish and click **Generate Project** again.
""")

    except Exception as e:

        st.error("❌ Project Generation Failed")

        with st.expander("Show Technical Details"):

            st.code(str(e))