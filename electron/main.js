const { app, BrowserWindow } = require('electron');
const path = require('path');
function createWindow(){
  const win = new BrowserWindow({ width: 1180, height: 820, webPreferences: { nodeIntegration:false }});
  win.loadFile(path.join(__dirname, '../web/index.html'));
}
app.whenReady().then(createWindow);
app.on('window-all-closed', ()=>{ if(process.platform!=='darwin') app.quit(); });
