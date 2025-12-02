# Provides styling to images once exported to html document
# Run this file once inside the project notebook using the %run magic command

from IPython.core.display import HTML

HTML("""
<style>
    div.output_area img, div.output_area svg {
        max-width: 100% !important;
        height: auto !important;
    }
</style>
""")
