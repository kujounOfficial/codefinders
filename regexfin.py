import re
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_function():
    # Get user input
    in_function = entry.get()
    if not in_function:
        messagebox.showerror("Input Error", "Please provide a regex pattern")
        return

    # Open a file dialog to select the input file
    input_file_path = filedialog.askopenfilename(title="Select Input File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not input_file_path:
        messagebox.showerror("File Error", "No input file selected")
        return

    # Open a file dialog to select the output file
    output_file_path = filedialog.asksaveasfilename(title="Select Output File", defaultextension=".txt", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not output_file_path:
        messagebox.showerror("File Error", "No output file selected")
        return
    
    try:
        # Read the file contents
        with open(input_file_path, 'r') as file:
            file_contents = file.readlines()
        
        # Compile the main regex pattern
        regex = re.compile(in_function)
        matches = []

        # Find all matches of the pattern
        for i, line in enumerate(file_contents):
            if regex.search(line):
                matches.append(i)

        # Debug: Print matches found
        print(f"Matches found at line indices: {matches}")

        # Check if matches are found
        if not matches:
            messagebox.showinfo("No Matches", "No matches found for the given regex pattern")
            return

        # Display the number of matches and ask for confirmation
        num_matches = len(matches)
        proceed = messagebox.askyesno("Matches Found", f"Found {num_matches} matches. Do you want to proceed with extraction?")
        if not proceed:
            return

        # Regular expression for function start and end
        start_pattern = re.compile(r"\w*FUN\w")  # Adjust this pattern as needed
        bad_start_pattern = re.compile(r"(?<!\S)=\s*\w*FUN\w*")
        bad_start_pattern2 = re.compile(r"\)\w*FUN")
        bad_start_pattern3 = re.compile(r"^\s*[^,\s]*FUN[^,\s]*\s*$")
        end_pattern = re.compile(r"^\}\s*$")

        # Extracting functions
        with open(output_file_path, 'w') as output:
            for match_index in matches:
                # Find the start of the function
                func_start = match_index
                while func_start >= 0:
                    if bad_start_pattern.search(file_contents[func_start]):
                        print("bad",func_start)
                    if not bad_start_pattern.search(file_contents[func_start]):
                        if not bad_start_pattern2.search(file_contents[func_start]):
                            if not bad_start_pattern3.search(file_contents[func_start]):
                                if start_pattern.search(file_contents[func_start]):
                                    print("good start",func_start)
                                    print("func name:  ",file_contents[func_start])
                                    break

                            
                    
                    func_start -= 1
                if func_start < 0:
                    continue  # Skip to next match if no function start found

                # Debug: Print function start line
                print(f"Function start found at line index: {func_start}")

                # Write the function content to output file
                line_index = func_start
                while line_index < len(file_contents):
                    output.write(file_contents[line_index])
                    if end_pattern.search(file_contents[line_index]):
                        print("end",line_index)
                        line_index += 1  # Include the line with the end pattern
                        break
                    line_index += 1

                # Debug: Print function lines being written
                print(f"Writing lines from {func_start} to {line_index}")

        messagebox.showinfo("Success", f"Function extracted and saved")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the Tkinter window
root = tk.Tk()
root.title("Function Extractor")

# Create and place the input field
tk.Label(root, text="Input Regex:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Create and place the Start button
start_button = tk.Button(root, text="Start", command=extract_function)
start_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
