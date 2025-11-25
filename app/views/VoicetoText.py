
def render_voice_page():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Live Voice to Text</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px}
    .row{margin-bottom:12px}
    #final{white-space:pre-wrap;border:1px solid #ddd;padding:12px;min-height:120px}
    #interim{color:#666;margin-top:8px}
    button{padding:8px 14px;margin-right:8px}
    label{margin-right:8px}
    #alert{color:red;margin-top:10px;font-weight:bold}
  </style>
</head>
<body>
  <h1>Live Voice to Text</h1>

  <div id="alert"></div>

  <div class="row">
    <label for="lang">Bahasa</label>
    <select id="lang">
      <option value="id-ID">Indonesia</option>
      <option value="en-US">English (US)</option>
    </select>
    <label><input type="checkbox" id="auto" checked> Auto-restart</label>
  </div>

  <div class="row">
    <button id="start">Mulai</button>
    <button id="stop" disabled>Berhenti</button>
    <span id="status">Siap</span>
  </div>

  <div class="row">
    <div id="final"></div>
    <div id="interim"></div>
  </div>

<script>

  // === DETEKSI SUPPORT BROWSER ===
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var alertEl = document.getElementById('alert');
  var startBtn = document.getElementById('start');

  if (!SR) {
      alertEl.innerHTML = "❌ Browser Anda tidak mendukung Web Speech API.<br>"
                        + "Gunakan <b>Google Chrome</b> agar fitur voice-to-text dapat berfungsi.";
      startBtn.disabled = true;
  }

</script>

<script>

  var statusEl = document.getElementById('status');
  var stopBtn = document.getElementById('stop');
  var finalEl = document.getElementById('final');
  var interimEl = document.getElementById('interim');
  var langSel = document.getElementById('lang');
  var autoChk = document.getElementById('auto');

  if (SR) {
    var rec = new SR();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = langSel.value;
    var started = false;

    rec.onstart = function(){
      statusEl.textContent = 'Mendengarkan...';
      startBtn.disabled = true;
      stopBtn.disabled = false;
    };

    rec.onend = function(){
      startBtn.disabled = false;
      stopBtn.disabled = true;
      statusEl.textContent = 'Sesi selesai';
      if(autoChk.checked && started){
        try{ rec.start(); }catch(e){}
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusEl.textContent = 'Mendengarkan...';
      }
    };

    startBtn.onclick = function(){
      statusEl.textContent = 'Meminta izin mikrofon...';
      var askMic = (navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
        ? navigator.mediaDevices.getUserMedia({audio:true})
        : Promise.resolve();

      askMic.then(function(stream){
        try {
          if(stream){ window._micStream = stream; }
          rec.lang = langSel.value;
          rec.start();
          started = true;
        } catch (err) {
          statusEl.textContent = 'Tidak bisa mulai: ' + err.message;
        }
      }).catch(function(err){
        statusEl.textContent = 'Izin mikrofon ditolak: ' + err.message;
      });
    };

    stopBtn.onclick = function(){
      rec.stop();
      started = false;
      startBtn.disabled = false;
      stopBtn.disabled = true;
      statusEl.textContent = 'Berhenti';
      try {
        if (navigator.mediaDevices && window._micStream) {
          window._micStream.getTracks().forEach(function(t){ t.stop(); });
          window._micStream = null;
        }
      } catch (e) {}
    };

    rec.onresult = function(e){
      var interim = '';
      var final = finalEl.textContent;
      for(var i= e.resultIndex; i< e.results.length; i++){
        var r = e.results[i];
        var t = r[0].transcript;
        if(r.isFinal){
          final += (final && final.slice(-1) !== '\\n' ? ' ' : '') + t + '\\n';
        } else {
          interim += t;
        }
      }
      finalEl.textContent = final;
      interimEl.textContent = interim;
    };

    rec.onerror = function(e){
      var msg = 'Error: ' + (e.error || 'unknown');
      if(e.error === 'not-allowed') msg += ' (izin mikrofon ditolak)';
      if(e.error === 'audio-capture') msg += ' (perangkat mikrofon tidak tersedia)';
      if(e.error === 'network') msg += ' (masalah jaringan layanan pengenalan)';
      statusEl.textContent = msg;
    };
  }
</script>

</body>
</html>
"""
