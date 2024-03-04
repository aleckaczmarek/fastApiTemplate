/* eslint-disable @typescript-eslint/no-explicit-any */

import { ReactNode, useEffect, useState } from 'react'
import classes from './App.module.css'

type ResponseType = { value: string, id:string, info?:{value: string, id:string, info?:ResponseType[]}[] }
type ResponseObjectArrayType = ResponseType[] | undefined

const getUUID = () => {
  return 'xxxxxxxx-xxxx-xxxx-yxxx-xxxxxxxxxxxx'
  .replace(/[xy]/g, function (c) {
      const r = Math.random() * 16 | 0, 
          v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
  });
}

const getObjectArraySplitUtil = (data?:string): ResponseObjectArrayType => {
  return data?.split("\n")?.map((value)=>{return {value:value, id:getUUID()}})
}

const changeItemToByUUIDWithValue = (uuid?:string, responseObjArray?:ResponseObjectArrayType, itemToChange?:ResponseObjectArrayType )=> {

  console.log(" [ getItemToChangeByUUId ] "+ uuid + " ",responseObjArray)
  responseObjArray?.forEach((item)=>{
    if(item?.id === uuid&&itemToChange) item['info'] = itemToChange
    else if(item?.info) changeItemToByUUIDWithValue(uuid,item?.info,itemToChange)
  })  

}
 

const getResponseJSX = ( onHandleSelected:(prompt:string, uuid:string) => void, selected?:string, responseObjArray?:ResponseObjectArrayType ): ReactNode => {
    return responseObjArray?.map((value): ReactNode => { 
      const className = value?.value?.slice(0,5)?.match(/[0-9]+\./) ? classes.numberTextBulletFormat : value?.value?.slice(0,5)?.match(/\*/) ? classes.numberTextAstricsFormat : classes.defaultTextReturnFormat;
      return (<div key={value.id}>
                <p  onClick={()=>onHandleSelected(value?.value,value?.id)} style={{border:selected===value?.id ?'1px solid black':'none'}} className={className} >
                    { value?.value + "\n" }
                </p>
                {getResponseJSX(onHandleSelected, selected, value.info)}
              </div>) 
      }) 
}

function App() { 
  const [sending,setSending] = useState(false)
  const [selected,setSelected] = useState<string>()
  const [response, setResponse] = useState<string>()
  const [question, setQuestion] = useState<string>()
  const [reprompt, setRepromp] = useState<string>()
  const [responseObjectsArray, setResponseObjectsArray] = useState<ResponseObjectArrayType>()


  useEffect(()=>{
        setResponseObjectsArray(getObjectArraySplitUtil(response))
  },[response]) 

  const getChatResponse = async (prompt?:string, uuid?:string, isReprompt?:boolean) => {
    if( !question && !prompt){
        window.alert("Please enter a question.") 
        return
      }
      try{
        setSending(true)
        const toAsk = prompt?prompt:question
        const urlToFetch = "/api/ai/ask/"+toAsk
        const response = await fetch(urlToFetch);
        const data = await response.json(); 
        if(isReprompt && responseObjectsArray && uuid !== null && uuid!== undefined){
          const newResp = [...responseObjectsArray]  
          changeItemToByUUIDWithValue(uuid, newResp, getObjectArraySplitUtil(data?.data))
          setResponseObjectsArray(newResp)
        } else {
          setRepromp('')
          setSelected(undefined)
          setResponse(data?.data)
        }
        setSending(false)
      } catch (e){
        setSending(false)
      }
    
  
  } 

  const onHandleSelected = (prompt:string, uuid:string) =>{
    setSelected(selected===uuid?"":uuid)
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

                {getResponseJSX(onHandleSelected, selected, responseObjectsArray)}
              
          </div>
        </div>
  )
}

export default App
