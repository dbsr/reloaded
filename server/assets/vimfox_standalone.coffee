### vimfox_standalone.js ~ initiates websocket / reload script ###
namespace = (target, name, block) ->
  [target, name, block] = [(if typeof exports isnt 'undefined' then exports else window), arguments...] if arguments.length < 3
  top    = target
  target = target[item] or= {} for item in name.split '.'
  block target, top

window.onload = ->
  vimfox.init()

namespace 'vimfox', (exports) ->
  vimfox.globals =
    RELOAD_PAGE: 0
    RELOAD_FILE: 1
    host: null
  vimfox.files = {}
  vimfox.init = ->
    # create the status element
    vimfox.status = new vimfox.Status()

    # get vimfox host information
    vimfox.globals.host = document.getElementById('vimfox-script')
      .getAttribute('src').replace(/\/vimfox\/vimfox_standalone.js/, '')

    # find all scripts / stylesheet elements with the vimfox data tag
    for element in document.getElementsByTagName('*')
      fpath = element.getAttribute('data-vimfox-path')
      if fpath?
        vimfox.files[fpath] = element

    # inject io if not in namespace
    if not io?
      s = document.createElement('script')
      s.type = 'text/javascript'
      s.onload = ->
        vimfox.setupSockets()
      s.src = "#{vimfox.globals.host}/vimfox/socket.io.min.js"
      document.body.appendChild(s)
    else
      vimfox.setupSockets()

  vimfox.setupSockets = ->
    console.log "'vimfox_standalone.coffee' :: 'window.onload' => 1"
    socket = io.connect("#{vimfox.globals.host}/ws")

    socket.on('connect', ->
      vimfox.status.update(0, 'OK!')
    )

    socket.on('error', (e) ->
      vimfox.status.update(2, e)
      console.error(e)
    )

    socket.on('disconnect', ->
      vimfox.status.update(1, 'disconnected')
      console.debug("socket disconnected")
    )

    # tell vimfox what files to watch on the local filesystem
    socket.emit('watch_files', Object.keys(vimfox.files))

    # now listen for reload commands
    socket.on('reload', (fname) ->
      f = vimfox.files[fname]
      if f?
        # reload the file if its a stylesheet
        console.log f.tagName
        if f.tagName == 'LINK'
          f.href = f.href.replace(/\?[0-9]+$/, "") + "?#{+new Date}"
        # else reload the page
        else
          location.reload()
    )

  class vimfox.Status
    constructor: ->
      d = document.createElement('div')
      d.id = "vimfox_status"
      document.body.appendChild(d)
      @me = document.getElementById('vimfox_status')
      @update(1)

    update: (status_code=0, tooltip="") ->
      status_color = [
        'green', 'orange', 'red'
      ][status_code]
      for k, v of {
          position: 'absolute',
          height: '10px',
          width: '10px',
          margin: '10px',
          top: '0',
          right: '0',
          backgroundColor: status_color}
        @me.style[k] = v

      @me.title = tooltip

    kill_me: ->
      document.body.removeChild(@me)
