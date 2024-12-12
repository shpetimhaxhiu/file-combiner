*# File Combiner

A Python script to combine multiple files into a single output file based on a customizable JSON configuration. This script supports features such as file grouping, headers, footers, and an optional Table of Contents (TOC).

## Features

- Combine files using file paths or glob patterns.
- Inspired by `vscode-combine-files` but built from scratch to address reliability issues and offer enhanced customization.
- Add custom headers and footers for each file group.
- Generate a Table of Contents with file paths and line numbers.
- Handle missing files gracefully with warnings.
- Supports logging for better debugging and usage monitoring.

## Requirements

- Python 3.7 or later


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shpetimhaxhiu/file-combiner.git
   cd file-combiner
   ```

> Note: The script actually doesn't require any external packages since it only uses Python's standard library modules. However, I've created a requirements.txt file anyway as it's good practice to have one.

## Usage

### Command-Line Arguments

```bash
python file_combiner.py --config <path_to_config> --output <output_file> [--debug]
```

#### Options

- `--config`, `-c`: Path to the JSON configuration file (default: `configfile.json`).
- `--output`, `-o`: Output file path (default: `combined_output.txt`).
- `--debug`, `-d`: Enable debug logging for detailed logs.

### Example

```bash
python file_combiner.py --config configfile.json --output combined.txt
```

## Configuration

The configuration file is a JSON file that specifies how files should be combined.

### Example `configfile.json`

```json
{
  "fileGroups": [
    {
      "files": [
        "./file1.txt",
      ],
      "fileHeader": [],
      "includeToc": true,
      "tocHeader": [
        "# Table of Contents",
        "# The following shows the line numbers and paths for included files:"
      ],
      "tocEntry": "# ${lineNo}\t\t${entryPath}",
      "tocFooter": [
        "# ============================================================"
      ],
      "entryHeader": [
        "### **${entryPath}**:",
        "",
        "---------------------------------------------",
        "",
        "```"
      ],
      "entryFooter": [
        "```",
        "",
        "---------------------------------------------",
        ""
      ],
      "fileFooter": [
        "",
        ""
      ]
    }
  ]
}
```

### Key Configuration Options

- `files`: List of specific file paths to include.
- `fileGlobs`: Use glob patterns to match files (e.g., `"*.txt"`).
- `fileHeader`, `fileFooter`: Add custom text before/after each file group.
- `entryHeader`, `entryFooter`: Add custom text before/after each file entry.
- `includeToc`: Boolean to include a Table of Contents.
- `tocHeader`, `tocFooter`, `tocEntry`: Customize TOC structure.

## Logging

Logs are written to `file_combiner.log` and also displayed on the console. Use the `--debug` flag for more detailed logs.

## Contribution

Feel free to fork the repository, make changes, and create pull requests. Suggestions and bug reports are welcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

> Created by Shpetim Haxhiu  
> [LinkedIn](https://linkedin.com/in/shpetimhaxhiu) | [GitHub](https://github.com/shpetimhaxhiu)