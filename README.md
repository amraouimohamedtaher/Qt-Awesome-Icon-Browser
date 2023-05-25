# Qt Awesome Icon Browser 
A modified standalone version of Icon Browser That's Built-in with PyQt5 

## Improvements :
[1] ui design
[2] much simpler code
[3] modified titlebar
## How To Use :

1 - open the app and select the prefered icon types listed on the title bar
2 - double click on the desired icon so you notice the change of status message 
3 - while the app is opened paste the app in your code after importing the icon package from foontawesome library  :

```python 
# import icon package
from qtawesome import icon
# adding icon to QToolButton
my_toolbutton = QToolButton( text = "this is tool button with custom icon" )
my_toolbutton.setIcon( icon("the_selected_icon_from_the_app") )
```
