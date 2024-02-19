
import { useState } from 'react'
import './App.css'

function App() { 

  const [sending,setSending] = useState(false)
  const [response, setResponse] = useState<string>()
  const [question, setQuestion] = useState<string>()

  const getChatResponse = async  () =>{
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
        <div style={{display:'flex', flexDirection:'column', width:'100%',height:'auto'}}> 
          <textarea onChange={(e)=>setQuestion(e.target.value)} style={{minHeight:'320px',margin:'auto', marginBottom:'32px', width:'90vw'}} />
          <button disabled={sending} onClick={getChatResponse} style={{margin:'auto', marginBottom:'32px', minHeight:'60px', minWidth:'300px', backgroundColor:'slategrey',color:'white',fontWeight:'900', fontSize:'28px' }}>🤖 Ask A Question 🤖</button>
          <div style={{whiteSpace:"pre-wrap", textAlign:'left',width:'100%', display:'flex', marginTop:'36px',flexDirection:'column'}}>{
            response?.split("\n").map((value)=>{
              if (!value.match(/[0-9]+\./)) return <span style={{ marginBottom:'16px'}}>{ value + ""}</span>
              else  return <p style={{ display:'block', marginLeft:'8px', marginBottom:'8px'}}>{ "\t" +  value  + "\n"}</p>
            })}
          </div>
        </div>
     
     
  )
}

export default App
