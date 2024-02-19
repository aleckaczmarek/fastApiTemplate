
import { useState } from 'react'

function App() { 

  const [sending,setSending] = useState(false)
  const [response, setResponse] = useState<string>()
  const [question, setQuestion] = useState<string>()

  const getChatResponse = async  () =>{
    if(!question){
        window.alert("Please enter a question.") 
        return
      }
    setSending(true)
    setResponse('')
    const response = await fetch("/api/ai/ask/"+question);
    const data = await response.json();
    console.log("data ", data)
    setResponse(data?.data)
    setSending(false)
  } 
  return ( 
        <div style={{
          display:'flex',
          flexDirection:'column', 
          width:'100%',
          height:'auto', 
          paddingBottom:'120px'}}
        > 
          <span style={{
            fontSize:'42px', 
            margin:'auto', 
            marginBottom:'24px', 
            marginTop:'8px' , 
            fontWeight:'600'}}>Welcome to Ask an Agent</span>
         <textarea 
              onChange={(e)=>setQuestion(e.target.value)} 
              style={{
                minHeight:'140px',
                margin:'auto', 
                marginBottom:'32px', 
                width:'90vw'}} 
          />
          <button 
              disabled={sending} 
              onClick={getChatResponse} 
              style={{
                     margin:'auto', 
                     borderRadius:'8px',
                     marginBottom:'32px', 
                     minHeight:'60px', 
                     minWidth:'300px', 
                     backgroundColor:'whitesmoke',
                     color:'black',
                     fontWeight:'600', 
                     fontSize:'28px' 
                     }}
          > 🤖 Ask Now 🤖</button>
       
          <div style={{ 
              whiteSpace:"pre-wrap", 
              textAlign:'left',
              margin:'auto',
              width:'90%', 
              display:'flex',
              flexDirection:'column'
              }}
          > 
          { response ? <>
                          <span style={{
                            fontSize:'32px', 
                            marginBottom:'16px'}}
                          >
                            Prompt 
                          </span> 
                          <i>{question}</i>
                          <span style={{
                            fontSize:'32px', 
                            marginTop:'16px', 
                            marginBottom:'-16px'}}
                          >
                            Response: 
                          </span> 
                        </> 
                      : 
                      null }
            {response?.split("\n").map((value)=>{
              if (value.match(/[0-9]+\./)) return <p  style={{ 
                                                                display:'flex', 
                                                                width:'90%', 
                                                                backgroundColor:'rgba(0,0,0,0.02)', 
                                                                margin:'auto', 
                                                                paddingLeft:'16px', 
                                                                paddingRight:'16px', 
                                                                paddingTop:'12px', 
                                                                paddingBottom:'12px', 
                                                                marginTop:'0px', 
                                                                marginBottom:'0px'}}
                                                    >
                                                      { value + "\n" }
                                                    </p>
              else if (value.match(/\*/)) return  <p  style={{ 
                                                                display:'flex', 
                                                                width:'90%', 
                                                                backgroundColor:'rgba(0,0,0,0.02)', 
                                                                margin:'auto', 
                                                                paddingLeft:'16px', 
                                                                paddingRight:'16px', 
                                                                paddingTop:'8px', 
                                                                paddingBottom:'8px', 
                                                                marginTop:'0px', 
                                                                marginBottom:'0px'}}
                                                    >
                                                      { value + "\n" }
                                                    </p>
              else                        return  <span style={{ 
                                                                marginBottom:'12px',
                                                                marginTop:'12px'}}
                                                    >
                                                        { value + ""}
                                                   </span>
            })} 
          </div>
        </div>
     
     
  )
}

export default App
