To be subclassed by application code.

  * Report : defines a set of data where users can work with.

  * PageLayout : defines how data fields and method buttons of a model or form are laid out in an entry form.
  * RowLayout : defines how data fields and method buttons of a model are laid out in an entry grid.

  * Action : something that will be done when a user clicks a button and/or hits a keystroke (or when a console script invokes it). An Action is always executed in a certain ActionContext.

For each Report subclass there will be one instance per site.

ActionContext : holds information that the Action needs about the outside world.

UI (User Interface Toolkit) : responsible for the user interface.
Stored in LinoSite.ui. Possible values are lino.ui.extjs.ui and lino.ui.console.ui
A UI must define the following functions:
  * get\_urls()
  * setup\_site(lino\_site)
  * get\_report\_url()
  * main\_panel\_class(layout)
  * (as well as the names Panel, StaticText, GridElement, MethodElement, field2elem,...)

ReportUI (rui) : a Report that has been set up for a UI. One instance per Report and UI. Instantiated lazily.

LayoutUI (lui) : a Layout that has been set up for a UI. One instance per Layout and UI.
Instantiated lazily.

ReportRequest : one instance per web request.
> .ui
> .report
> .queryset : the Django queryset



| rd | report definition |
|:---|:------------------|
| rh | report handle     |
| rr | report request    |