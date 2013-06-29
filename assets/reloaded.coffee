### reloaded_standalone.js ~ initiates websocket / reload script ###
namespace = (target, name, block) ->
  [target, name, block] = [(if typeof exports isnt 'undefined' then exports else window), arguments...] if arguments.length < 3
  top    = target
  target = target[item] or= {} for item in name.split '.'
  block target, top

window.onload = ->
  reloaded.init()

namespace 'reloaded', (exports) ->
  reloaded.globals =
    RELOAD_PAGE: 0
    RELOAD_FILE: 1
    host: null
  reloaded.files = {}
  reloaded.init = ->
    # create the status element
    reloaded.status = new reloaded.Status()

    # get reloaded host information
    element = document.getElementById('reloaded-script')
    unless element?
      for script in document.getElementsByTagName("script")
        if script.getAttribute('src') and script.getAttribute('src').match(/reloaded.js/)
          element = script
          break
    reloaded.globals.host = element.getAttribute('src')
      .replace(/\/reloaded\/reloaded.js/, '')

    # find all scripts / stylesheet elements with the reloaded data tag
    for element in document.getElementsByTagName('*')
      fpath = element.getAttribute('data-reloaded-path')
      if fpath?
        reloaded.files[fpath] = element

    # inject io if not in namespace
    if not io?
      s = document.createElement('script')
      s.type = 'text/javascript'
      s.onload = ->
        reloaded.setupSockets()
      s.src = "#{reloaded.globals.host}/reloaded/socket.io.min.js"
      document.body.appendChild(s)
    else
      reloaded.setupSockets()

  reloaded.setupSockets = ->
    console.log "'reloaded_standalone.coffee' :: 'window.onload' => 1"
    socket = io.connect("#{reloaded.globals.host}/ws")

    socket.on('connect', ->
      reloaded.status.update(0, 'OK!')
    )

    socket.on('error', (e) ->
      reloaded.status.update(2, e)
      console.error(e)
    )

    socket.on('disconnect', ->
      reloaded.status.update(1, 'disconnected')
      console.debug("socket disconnected")
    )

    # tell reloaded what files to watch on the local filesystem
    socket.emit('watch_files', Object.keys(reloaded.files))

    # now listen for reload commands
    socket.on('reload', (fname) ->
      f = reloaded.files[fname]
      if f?
        # reload the file if its a stylesheet
        console.log f.tagName
        if f.tagName == 'LINK'
          f.href = f.href.replace(/\?[0-9]+$/, "") + "?#{+new Date}"
        # else reload the page
        else
          location.reload()
    )

  class reloaded.Status
    constructor: ->
      d = document.createElement('div')
      d.id = "reloaded_status"
      document.body.appendChild(d)
      @me = document.getElementById('reloaded_status')
      for k, v of {
          position: 'absolute',
          height: '15px',
          width: '15px',
          margin: '15px',
          top: '0',
          right: '0',
          zIndex: '999999'}
        @me.style[k] = v
      @update(1)

    update: (status_code=0, tooltip="") ->
      status_color = [
        'green', 'orange', 'red'][status_code]
      @me.style['backgroundColor'] = status_color
      @me.title = tooltip

    kill_me: ->
      document.body.removeChild(@me)
