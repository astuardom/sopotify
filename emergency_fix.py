"""
Script to fix the corrupted index.html file
"""
import re

def fix_html_corruption():
    html_path = 'templates/index.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove the duplicated content at the end (</html></body></html>...)
    # Find the last </html> and keep everything before it
    if content.count('</html>') > 1:
        last_html = content.rfind('</html>')
        # Find the second to last </html>
        second_last = content.rfind('</html>', 0, last_html)
        if second_last != -1:
            content = content[:second_last+7]
            print("✓ Removed duplicated HTML end tags")

    # 2. Fix startDownload function
    # It seems to have missing variables and potentially duplicated parts
    
    start_download_fixed = """    async function startDownload() {
        const url = document.getElementById('spotify-url').value.trim();
        const statusArea = document.getElementById('status-area');
        const statusText = document.getElementById('status-text');
        
        if (!url) return;
        
        statusArea.classList.remove('hidden');
        statusText.innerText = "Starting...";
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: url
                })
            });
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            if (data.message) statusText.innerText = data.message;
                            if (data.status === 'completed') loadLibrary();
                        } catch (e) { }
                    }
                }
            }
            
            statusText.innerText = "Done!";
            setTimeout(() => statusArea.classList.add('hidden'), 3000);
        } catch (e) {
            console.error(e);
            statusText.innerText = "Error: " + e.message;
        }
    }"""

    # Replace the broken function with the fixed one
    # We'll use regex to find the function, handling the mess
    pattern = r"async function startDownload\(\)\s*\{[\s\S]*?^\s*\}\s*catch"
    
    # Since the file is messy, let's try to locate the function start and replace until the next function or end of script
    # But a safer bet might be to just replace the whole script section if we can identify it
    
    # Let's try a simpler approach: Find the startDownload definition and replace it
    # The current file has a mess around startDownload. 
    
    # Let's read the file line by line and reconstruct the script part
    lines = content.split('\n')
    new_lines = []
    in_script = False
    in_start_download = False
    script_lines = []
    
    for line in lines:
        if '<script>' in line:
            in_script = True
            new_lines.append(line)
            continue
            
        if '</script>' in line:
            in_script = False
            # Process the accumulated script lines
            # ...
            new_lines.append(start_download_fixed) # We'll just append our fixed function and other functions
            # This is too risky without parsing.
            
    # Alternative: Just replace the specific broken block we know about
    # The broken block has:
    # async function startDownload() {
    #    if (!url) return;
    
    broken_start = "async function startDownload() {\n        if (!url) return;"
    if broken_start in content:
        content = content.replace(broken_start, start_download_fixed.split('\n')[0] + "\n" + start_download_fixed.split('\n')[1] + "\n" + start_download_fixed.split('\n')[2] + "\n" + start_download_fixed.split('\n')[3] + "\n        if (!url) return;")
        # This is getting complicated.
        
    # Let's use the replace method with a large chunk of context
    # We know what the broken part looks like from the diff
    
    # It looks like there are multiple startDownload or fragments.
    # Let's just rewrite the file with a known good state for the script part if possible.
    
    # Let's try to find the startDownload function and replace it entirely
    # We will look for "async function startDownload() {" and find the matching closing brace
    
    # Actually, the previous tool output showed a huge duplication.
    # Let's just use the "fix_html_pwa.py" logic but implemented here since we can't edit that file easily
    
    # ... (implementation of clean up)
    pass

def clean_and_fix():
    html_path = 'templates/index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Clean up duplicate HTML tags at the end
    # The file likely ends with </html></body></html>...
    if content.count('</html>') > 1:
        # Keep only up to the first </html>
        end_idx = content.find('</html>') + 7
        content = content[:end_idx]
        print("✓ Truncated after first </html>")
        
    # 2. Fix the startDownload function
    # We'll search for the function and replace it with the correct version
    
    correct_function = """    async function startDownload() {
        const url = document.getElementById('spotify-url').value.trim();
        const statusArea = document.getElementById('status-area');
        const statusText = document.getElementById('status-text');
        
        if (!url) return;
        
        statusArea.classList.remove('hidden');
        statusText.innerText = "Starting...";
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: url
                })
            });
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            if (data.message) statusText.innerText = data.message;
                            if (data.status === 'completed') loadLibrary();
                        } catch (e) { }
                    }
                }
            }
            
            statusText.innerText = "Done!";
            setTimeout(() => statusArea.classList.add('hidden'), 3000);
        } catch (e) {
            console.error(e);
            statusText.innerText = "Error: " + e.message;
        }
    }"""
    
    # Regex to replace the existing (possibly broken) function
    # We match from "async function startDownload" until the next function definition or end of script
    # This is a heuristic
    
    # First, let's remove the broken version that starts with "if (!url) return;" immediately
    broken_pattern = r"async function startDownload\(\)\s*\{\s*if \(!url\) return;"
    
    if re.search(broken_pattern, content):
        print("✓ Found broken startDownload, replacing...")
        # We need to be careful about where the function ends. 
        # Since the file is messy, let's try to replace the whole script block if we can find the boundaries of startDownload
        
        # Let's try a simpler replacement:
        # Find the broken function start
        start_idx = re.search(broken_pattern, content).start()
        
        # Find the end of this function (counting braces)
        brace_count = 0
        end_idx = start_idx
        found_brace = False
        
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
                found_brace = True
            elif content[i] == '}':
                brace_count -= 1
            
            if found_brace and brace_count == 0:
                end_idx = i + 1
                break
        
        # Replace
        content = content[:start_idx] + correct_function + content[end_idx:]
        
    # Also check for the other broken pattern where variables are missing but it doesn't start with if(!url)
    # or if there are multiple copies
    
    # Let's just make sure the correct function is there and no duplicates
    # This is hard with regex.
    
    # Let's try to just write the file with the correct content if we can identify the structure
    # The file structure is: HTML -> Script -> Functions
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✓ HTML cleanup finished")

if __name__ == "__main__":
    clean_and_fix()
