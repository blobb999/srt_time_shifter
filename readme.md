![srt_time_shifter](https://github.com/user-attachments/assets/bea31189-0d3a-4521-a298-85e79baef845)
SRT Time Shifter

SRT Time Shifter is a simple and intuitive tool for shifting the timing of subtitles in .srt files. Whether your subtitles are appearing too early or too late, this app allows you to adjust the timing with ease. The app supports both positive and negative time shifts, so you can move subtitles forward or backward in time.
Features

    Shift Subtitle Timing: Move subtitles forward or backward by specifying the shift in seconds.
    Batch Process: Shift an entire .srt file at once.
    Overwrite Option: Choose to overwrite the original file or save the shifted file separately.
    Simple Interface: User-friendly interface with easy file and directory selection.
    Tooltip Assistance: Tooltips guide you on how positive and negative shifts affect your subtitles.
    Multi-language Support: Switch between English and German (more languages can be added).

Requirements

    Python 3.x
    tkinter for the graphical user interface (should come pre-installed with Python)

No external dependencies required beyond the standard Python libraries.
Installation

    Clone this repository to your local machine:

    bash

git clone https://github.com/yourusername/srt-time-shifter.git

Navigate to the project directory:

bash

cd srt-time-shifter

Run the application:

bash

    python srt_time_shifter.py

Usage

    Open SRT File: Click the "Browse" button to select the .srt file you want to shift.
    Set Output Directory (optional): Choose where the modified file should be saved. If you prefer to overwrite the original file, enable the "Overwrite original file" option.
    Enter Time Shift: Specify how many seconds you'd like to shift the subtitles by. Positive values delay subtitles, while negative values make them appear earlier.
    Shift SRT: Click the "Shift SRT" button to process the file.
    Success: Once the process is complete, a message will confirm the file has been saved.

Example

    Positive Shift (+8 seconds): Subtitles will appear 8 seconds later than their original timing.
    Negative Shift (-8 seconds): Subtitles will appear 8 seconds earlier than their original timing.

Screenshots

Icon

The app icon represents time manipulation and subtitle editing, combining a clock with subtitle symbols, such as a film strip or text.
Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

    Fork the repo
    Create your feature branch (git checkout -b feature/fooBar)
    Commit your changes (git commit -m 'Add some fooBar')
    Push to the branch (git push origin feature/fooBar)
    Open a Pull Request

License

This project is licensed under the MIT License. See the LICENSE file for more details.