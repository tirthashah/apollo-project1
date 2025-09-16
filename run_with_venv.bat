@echo off
cd /d C:\Users\X1\Selenium\apollo

echo [+] Activating virtual environment...
call myenv\Scripts\activate

echo [+] Running the Python script...
REM We add the required arguments to the end of this line
python name_gen.py --account "Brijesh" --action "both" --file "result.xlsx"

echo [+] Deactivating virtual environment...
deactivate

echo.
echo [+] --- Script finished. Press any key to close this window... ---
pause