
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
  // const vartosplit = "\nHere are a few options for making the mission statement sound more engaging:\n\n1. \"Empowering trust and collaboration in the digital marketplace, connecting consumers with top-rated service providers for unparalleled experiences.\"\n2. \"Creating a safe and secure platform where consumers can confidently find and work with the best service providers, fostering long-term relationships and growth for all parties involved.\"\n3. \"Transforming the way people connect and transact, building a trusted marketplace that redefines the future of commerce and community.\"\n4. \"Unlocking the potential of the digital economy by facilitating authentic and meaningful interactions between consumers and service providers, driving growth and innovation for all stakeholders.\"\n5. \"Elevating the way people buy and sell services online, fostering a culture of trust, collaboration, and mutual success across our global community.\"\n6. \"Creating an ecosystem where consumers can find, compare, and book top-rated service providers with ease, while service providers can grow their businesses through our powerful platform.\"\n7. \"Bringing people together to exchange value and build lasting relationships in a trustworthy and convenient marketplace, leveraging the power of technology to drive growth and success.\"\n8. \"Forging a community that values trust, transparency, and mutual respect between consumers and service providers, while fostering innovation and collaboration in the digital economy.\"\n9. \"Elevating the way people buy, sell, and share services online, by building a platform that prioritizes trust, convenience, and value for all stakeholders.\"\n10. \"Transforming the way we think about commerce, by creating an inclusive and secure marketplace where consumers can find and work with top-rated service providers, while fostering collaboration and growth for all parties involved.\"\n\nThese revised mission statements aim to make the original statement more engaging and memorable, while still conveying the core values and goals of the company."
  return ( 
        <div style={{display:'flex',flexDirection:'column', width:'100%',height:'auto', paddingBottom:'120px'}}> 
          <span style={{fontSize:'42px', margin:'auto', marginBottom:'24px', marginTop:'8px' , fontWeight:'600'}}>Welcome to Ask an Agent</span>
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
                              <span style={{fontSize:'32px', marginBottom:'16px'}}>
                               Prompt 
                              </span> 
                              <i>{question}</i>
                              <span style={{fontSize:'32px', marginTop:'16px', marginBottom:'-16px'}}>
                                Response: 
                              </span> 
                          </> 
                        : 
                        null }

            {response?.split("\n").map((value)=>{
              if (value.match(/[0-9]+\./)) return <p  style={{ display:'flex', width:'90%', backgroundColor:'rgba(0,0,0,0.02)', margin:'auto', paddingLeft:'16px', paddingRight:'16px', paddingTop:'12px', paddingBottom:'12px', marginTop:'0px', marginBottom:'0px'}}>{ "" +  value  + "\n"}</p>
              else if (value.match(/\*/)) return  <p  style={{ display:'flex', width:'90%', backgroundColor:'rgba(0,0,0,0.02)', margin:'auto', paddingLeft:'16px', paddingRight:'16px', paddingTop:'8px', paddingBottom:'8px', marginTop:'0px', marginBottom:'0px'}}>{ "" +  value  + "\n"}</p>
              else  return <span style={{ marginBottom:'12px',marginTop:'12px'}}>{ value + ""}</span>
            })}

          </div>
        </div>
     
     
  )
}

export default App
