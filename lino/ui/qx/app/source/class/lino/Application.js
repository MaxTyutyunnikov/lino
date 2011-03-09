/* ************************************************************************

   Copyright:

   License:

   Authors:

************************************************************************ */

/* ************************************************************************

#asset(lino/*)

************************************************************************ */

/**
 * This is the main application class of your custom application "lino"
 */
qx.Class.define("lino.Application",
{
  extend : qx.application.Standalone,



  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    main : function()
    {
      // Call super class
      this.base(arguments);

      // Enable logging in debug variant
      if (qx.core.Variant.isSet("qx.debug", "on"))
      {
        // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Native;
        // support additional cross-browser console. Press F7 to toggle visibility
        qx.log.appender.Console;
      }

      /*
      -------------------------------------------------------------------------
        Below is your actual application code...
      -------------------------------------------------------------------------
      */
      
      //~ var main = new lino.MainWindow();
      //~ main.maximize();
      //~ main.open(); 
      
      //~ var service = new hello.TwitterService();
      //~ service.addListener("changeTweets", function(e) {
        //~ this.debug(qx.dev.Debug.debugProperties(e.getData()));
      //~ }, this);
      //~ service.addListener("postOk", function() {
        //~ main.clearPostMessage();
        //~ service.fetchTweets();
      //~ }, this);
       
      //~ main.addListener("reload", function() {
        //~ this.debug("reload");
        //~ service.fetchTweets();
      //~ }, this);

      //~ main.addListener("post", function(e) {
        //~ this.debug("post: " + e.getData());
        //~ service.post(e.getData());
      //~ }, this);      
      
      //~ var controller = new qx.data.controller.List(null, main.getList());      
      //~ controller.setLabelPath("text");
      //~ controller.setIconPath("user.profile_image_url");
      //~ controller.setDelegate({
        //~ configureItem : function(item) {
          //~ item.getChildControl("icon").setWidth(48);
          //~ item.getChildControl("icon").setHeight(48);
          //~ item.getChildControl("icon").setScale(true);
          //~ item.setRich(true);
        //~ }
      //~ });      
      //~ controller.setDelegate({
        //~ createItem : function() {
          //~ return new hello.TweetView();
        //~ },
        //~ bindItem : function(controller, item, id) {
          //~ controller.bindProperty("text", "post", null, item, id);
          //~ controller.bindProperty("user.profile_image_url", "icon", null, item, id);
          //~ controller.bindProperty("created_at", "time", {
            //~ converter: function(data) {
             //~ if (qx.bom.client.Engine.MSHTML) {
               //~ data = Date.parse(data.replace(/( \+)/, " UTC$1"));
             //~ }
             //~ return new Date(data);
           //~ }
          //~ }, item, id);
        //~ },
        
        
        //~ configureItem : function(item) {
          //~ item.getChildControl("icon").setWidth(48);
          //~ item.getChildControl("icon").setHeight(48);
          //~ item.getChildControl("icon").setScale(true);
          //~ item.setRich(true);
          //~ item.setMinHeight(52);
        //~ }
      //~ });      
      //~ service.bind("tweets", controller, "model");
      
      
      //~ this.__loginWindow = new hello.LoginWindow();
      //~ this.__loginWindow.moveTo(320,30);
      //~ this.__loginWindow.open();
      
      //~ this.__loginWindow.addListener("changeLoginData", function(ev) {
        //~ var loginData = ev.getData();
        //~ service.fetchTweets(loginData.username, loginData.password);
      //~ });
      
      
      //~ service.fetchTweets();

      //~ // Create a button
      //~ var button1 = new qx.ui.form.Button("Hello", "hello/test.png");

      //~ // Document is the application root

      //~ // Add button to document at fixed coordinates
      //~ doc.add(button1, {left: 100, top: 50});

      //~ // Add an event listener
      //~ button1.addListener("execute", function(e) {
        //~ alert("Hello World!");
      //~ });
      
      //~ var req = new qx.io.remote.Request('http://127.0.0.1:8000/menu', "GET", "application/json");
      var req = new qx.io.remote.Request('/menu', "GET", "application/json");
      req.addListener("completed", this.onMenuCompleted, this);
      //~ req.addListener("completed", function(e) {
          //~ this.loadMenu(e.getContent())
      //~ });
      req.send();
    },
    
    onMenuCompleted : function(e) {
      //~ console.log(e);
      //~ this.debug(e.getStatusCode());
    
      var toolBar = new qx.ui.toolbar.ToolBar();
      this.getRoot().add(toolBar, {
        left: 0,
        top: 0,
        right: 0
      });
      
      var response = e.getContent();
      console.log(response);
      for (var i = 0; i < response.load_menu.length; i++) {
          var mi = response.load_menu[i];
          if (mi.menu) {
              var mb = new qx.ui.toolbar.MenuButton(mi.text);
              toolBar.add(mb);
              var m = new qx.ui.menu.Menu();
              for (var j = 0; j < mi.menu.items.length; j++) {
                  m.add(new qx.ui.menu.Button(mi.menu.items[j].text));
              }
              mb.setMenu(m);
          }
      }
      
      //~ var m = new qx.ui.menu.Menu();
      //~ var command = new qx.ui.core.Command("Control+P");
      //~ command.addListener("execute", function() {
        //~ this.debug("Persons");
      //~ },this);
      //~ m.add(new qx.ui.menu.Button("Persons", null, command));
      //~ m.add(new qx.ui.menu.Separator());
      //~ m.add(new qx.ui.menu.Button("Exit"));
      //~ mb.setMenu(m);
      
    }
  }
});


