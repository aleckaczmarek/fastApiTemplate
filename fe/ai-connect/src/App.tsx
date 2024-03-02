
import { useEffect, useState } from 'react'
import classes from './App.module.css'

function App() { 

  const [sending,setSending] = useState(false)
  const [selected,setSelected] = useState<number>()
  const [response, setResponse] = useState<string>()
  const [question, setQuestion] = useState<string>()
  const [reprompt, setRepromp] = useState<string>()
  const [responseObjectsArray, setResponseObjectsArray] = useState<{ [x: number]: string; }[] | undefined>()

  useEffect(()=>{
        setResponseObjectsArray(response?.split("\n")?.map((value, index)=>{return {[index]:value}}))
  },[response]) 
  const getChatResponse = async (prompt?:string, index?:number, isReprompt?:boolean) => {
    if( !question && !prompt){
        window.alert("Please enter a question.") 
        return
      }
    setSending(true)
    
    const toAsk = prompt?prompt:question
    const urlToFetch = "/api/ai/ask/"+toAsk
    const response = await fetch(urlToFetch);
    const data = await response.json();
    if(isReprompt && responseObjectsArray && index !== null && index!== undefined){
      const newResp = [...responseObjectsArray]
      newResp[index][index] = data?.data
      setResponseObjectsArray(newResp)
    } else {
      setResponse(data?.data)
    }
    setSending(false)
  } 

  const onHandleSelected = (prompt:string, index:number) =>{
    setSelected(selected===index?-1:index)
    setRepromp("Tell me more about \n \n"+prompt)
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
              onClick={async () => await getChatResponse(question)} 
              className={classes.chatNowButton} > 
              🤖 Ask Now 🤖
          </button> 
          <div style={{ whiteSpace:"pre-wrap", textAlign:'left', margin:'auto', width:'90%', display:'flex', flexDirection:'column' }} > 
              { responseObjectsArray ? <>
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
                {selected !== null ? <>
                  <textarea 
                            value={reprompt}
                            onChange={(e)=>setRepromp(e.target.value)} 
                            className={classes.chatText} />
                        <button 
                            disabled={sending} 
                            onClick={async () => await getChatResponse(reprompt, selected, true)} 
                            className={classes.chatNowButton} > 
                            🤖 Reprompt this selection now 🤖
                        </button> 
                            </>
                              :
                  null
                }
                { responseObjectsArray?.map((value,index)=>{
                        if (value[index]?.slice(0,5)?.match(/[0-9]+\./)) return <p onClick={()=>onHandleSelected(value[index],index)} style={{border:selected===index?'1px solid black':'none'}} className={ classes.numberTextBulletFormat } >
                                                                { value[index] + "\n" }
                                                            </p>
                        else if (value[index]?.slice(0,5)?.match(/\*/)) return  <p onClick={()=>onHandleSelected(value[index],index)} style={{border:selected===index?'1px solid black':'none'}}  className={ classes.numberTextAstricsFormat } >
                                                                { value[index] + "\n" }
                                                            </p>
                        else                        return  <span onClick={()=>onHandleSelected(value[index],index)} style={{border:selected===index?'1px solid black':'none'}} className={ classes.defaultTextReturnFormat } >
                                                                { value[index] + ""}
                                                            </span>
                        }) 
                } 
          </div>
        </div>
  )
}

export default App
