This is my personal summary of the [ExtJS documentation](http://www.extjs.com/deploy/dev/docs/).

Every Container (Ext.Window, Ext.Panel) should have a config option 'layout' which specifies the LayoutManager of this container. The LayoutManager is responsible for telling the Container's children their size.

Some LayoutManagers support themselves configuration options. You can specify these using the Container's 'layoutConfig' option.

Useful values for 'layout' are:

## border ##

Splits the container into "regions" (center, north, south...)
Each elements should have a config option 'region'.
For each region there should be at most one element.
At least the 'center' must get an element, all other regions are optional.

## fit ##
Works only on containers that have a single element. Sizes the single element so that it fills the container's space.

## hbox and vbox ##

These layout managers stacks the elements in a row, either horizontally or vertically. Elements should have config options 'flex' and 'margins'. The container's 'layoutConfig' can contain:
  * align : how the elements are aligned in case their heights differ. Allowed values are
    * for 'hbox': 'top', 'middle', 'stretch' and 'stretchmax'
    * for 'vbox': 'left', 'center', 'stretch' and 'stretchmax'
  * defaultMargins : margin value to use as default for contained elements that don't have their own 'margins' property. Default value: {top:0, right:0, bottom:0, left:0}
  * pack : how the elements are packed together. Allowed values are 'start', 'center', and 'end'.

## anchor ##

Contained elements are anchored relative to the container's dimensions. If the container is resized, all anchored items are automatically rerendered according to their anchor rules.
Elements should have a config option 'anchor'.

## form ##

A subclass of 'anchor'. It is the only layout able to render fieldLabels. The container's 'layoutConfig' can contain:
  * labelAlign : ("left", "top" or "right")
  * labelPad : padding between label and element
  * labelSeparator : the string to place after the label. Default is ":". This property can be specified at layout, container or component level.
  * labelWidth
  * hideLabels