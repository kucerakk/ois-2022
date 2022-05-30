extensions = [
    'sphinx_revealjs'
]

revealjs_static_path = ['_static']
revealjs_css_files = ['custom.css', 'revealjs4/plugin/highlight/monokai.css']
revealjs_script_plugins = [
    {
            "src": "revealjs4/plugin/highlight/highlight.js",
            "name": "RevealHighlight",
    },
   ]

revealjs_script_conf = """
{
    controls: true,
    controlsBackArrows: 'faded',
    transition: 'slide',
    // Display a presentation progress bar
    progress: true,
    //width: '90%',
    // Factor of the display size that should remain empty around
    // the content
    margin: 0.04,
    // Bounds for smallest/largest possible scale to apply to content
    minScale: 0.2,
    maxScale: 2.0,
    width: 1600,
    height: 800,
}
"""
