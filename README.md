# 1Password
Convert [SafeInCloud](https://safe-in-cloud.com/) XML file to [1Passsord](https://1password.com) CSV file.  
**WHY?** Because the SafeInCloud CSV export file does not export TAGs, and I have a lot of them :worried:
```
python sic_to_1password.py

Safe in Cloud XML => 1Password CSV
python sic_to_1password.py SafeInCloud.xml 1Password.csv
```
1. Export SafeInCloud XML file
2. Convert file
3. Import 1Password CSV file mapping the following fields
```
title
login
password
website
notes
label
```
If you want to avoid some SafeInCloud entries to be imported change the code below (commented out by default):
```python
# DO NOT Convert some accounts
if title.startswith('Z '):
    print(title)
    continue
```
After importing a TAG like **Imported august 17 2024 17:16:07** will be created.  
To delete it you have to install the 1Password DESKTOP version, right click on the TAG at left side menu and delete.  
Hope you enjoy :smiley:
