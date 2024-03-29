Special model attributes and methods
------------------------------------

See :class:`lino.core.model.Model`

.. modattr:: _lino_preferred_width

    Used to set an explicit default `preferred_width` (in characters) 
    for ForeignKey fields to this model. 
    If not specified, the default default `preferred_width` 
    for ForeignKey fields is *20*.
    
.. modattr:: _lino_default_table

    Used internally. Lino chooses during the kernel startup, for each model, 
    one of the discovered Table subclasses as the "default table".

    
    
.. modattr:: disabled_fields

    return a list of names of fields that should be disabled (not editable) 
    for this record.
    
    Example::
    
      def disabled_fields(self,request):
          if self.user == request.user: return []
          df = ['field1']
          if self.foo:
            df.append('field2')
          return df
        
.. modattr:: disable_delete

    Hook to decide whether a given record may be deleted.
    Return a non-empty string with a message that explains why this record cannot be deleted.
    
    Example::
    
      def disable_delete(self,request):
          if self.is_imported:
              return _("Cannot delete imported records.")
            
        
.. modattr:: disable_editing

  ``disable_editing(self,request)``
      Return `True` if the whole record should be read-only.


.. modattr:: FOO_choices

  Return a queryset or list of allowed choices for field FOO.
  Must be decorated by a :func:`lino.utils.choosers.chooser`.
  Example of a context-sensitive chooser method::
  
      
      country = models.ForeignKey("countries.Country",blank=True,null=True,
          verbose_name=_("Country"))
      city = models.ForeignKey('countries.City',blank=True,null=True,
          verbose_name=_('City'))
          
      @chooser()
      def city_choices(cls,country):
          if country is not None:
              return country.city_set.order_by('name')
          return cls.city.field.rel.to.objects.order_by('name')
      
  

.. modattr:: FOO_changed

    Called when field FOO of an instance of this model has been modified through the user interface.
    Example::
    
      def city_changed(self,oldvalue):
          print "City changed from %s to %s!" % (oldvalue,self.city)

    
.. modattr:: get_queryset

    Return a customized default queryset
    
    Example::

      def get_queryset(self):
          return self.model.objects.select_related('country','city','coach1','coach2','nationality')


.. modattr:: data_control

  Used by :class:`lino.models.DataControlListing`.
    
  Example::

      def data_control(self):


.. modattr:: on_user_change

  Called when a record has been modified through the user interface.
    
  Example::
  
    def on_user_change(self,request):


.. modattr:: save_auto_tasks

  Example::
  
    def save_auto_tasks(self):


.. modattr:: setup_report

  Example::

      @classmethod
      def setup_report(model,rpt):

.. modattr:: summary_row

  Return a HTML fragment that describes this record in a 
  :func:`lino.core.tables.summary`.
  
  Example::
  
    def summary_row(self,ui,rr,**kw):
        s = ui.href_to(self)
        if settings.LINO.projects_model:
            if self.project and not reports.has_fk(rr,'project'):
                s += " (" + ui.href_to(self.project) + ")"
        return s
  


.. modattr:: update_owned_task

  Example::
  
    def update_owned_task(self,task):
        task.person = self


