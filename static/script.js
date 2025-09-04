async function sendMessage(){
    let msg=document.getElementById("msg").value;
    document.getElementById("msg").value='';
    let resp=await fetch('/webchat',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({text:msg})
    });
    let data=await resp.json();
    let chat=document.getElementById("chatbox");
    chat.innerHTML+="<div><b>You:</b> "+msg+"</div><div><b>Bot:</b> "+data.reply+"</div>";
}

async function uploadFile(){
    let fi=document.getElementById("fileinput");
    if(!fi.files.length) return;
    let fd=new FormData(); fd.append('file',fi.files[0]);
    let res=await fetch('/upload',{method:'POST',body:fd});
    let data=await res.json();
    document.getElementById("chatbox").innerHTML+="<div>Uploaded: "+data.filename+"</div>";
      }
