
import { useState } from 'react'
import classes from './App.module.css'

function App() { 

  const [sending,setSending] = useState(false)
  const [response, setResponse] = useState<string>()
  const [question, setQuestion] = useState<string>()

  const getChatResponse = async () => {

    if( !question ){
        window.alert("Please enter a question.") 
        return
      }

    setSending(true)
    setResponse('')
    const response = await fetch("/api/ai/ask/"+question);
    const data = await response.json();
    setResponse(data?.data)
    setSending(false)
  } 

  return ( 
        <div style={{ display:'flex', flexDirection:'column', width:'100%',  height:'auto', paddingBottom:'120px'}} > 
          <span className={classes.welcomeHeader}>
            Welcome to Ask an Agent
          </span>
         <textarea 
              onChange={(e)=>setQuestion(e.target.value)} 
              className={classes.chatText} />
          <button 
              disabled={sending} 
              onClick={getChatResponse} 
              className={classes.chatNowButton} > 
              🤖 Ask Now 🤖
          </button> 
          <div style={{ whiteSpace:"pre-wrap", textAlign:'left', margin:'auto', width:'90%', display:'flex', flexDirection:'column' }} > 
              { response ? <>
                              <span style={{ fontSize:'32px', marginBottom:'16px' }} >
                                Prompt 
                              </span> 
                              <i>
                                {question}
                              </i>
                              <span style={{ fontSize:'32px', marginTop:'16px', marginBottom:'16px' }} >
                                Response: 
                              </span> 
                            </> 
                          : 
                  null 
                }
                { response?.split("\n")?.map((value)=>{
                        if (value?.slice(0,5)?.match(/[0-9]+\./)) return <p className={ classes.numberTextBulletFormat } >
                                                                { value + "\n" }
                                                            </p>
                        else if (value?.slice(0,5)?.match(/\*/)) return  <p  className={ classes.numberTextAstricsFormat } >
                                                                { value + "\n" }
                                                            </p>
                        else                        return  <span className={ classes.defaultTextReturnFormat } >
                                                                { value + ""}
                                                            </span>
                        }) 
                } 
          </div>
        </div>
  )
}

export default App
