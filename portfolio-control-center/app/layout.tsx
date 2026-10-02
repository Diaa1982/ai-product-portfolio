import type { Metadata } from "next"; import "./globals.css";
const description="Connect strategy, performance, processes, services, governance and AI to assess organizational maturity, identify improvement opportunities and turn intelligence into measurable action.";
export const metadata:Metadata={title:"Enterprise Transformation & AI Solutions | Transformation Intelligence",description,openGraph:{title:"Transform Your Organization. Powered by Intelligence.",description,type:"website"},twitter:{card:"summary_large_image",title:"Transform Your Organization. Powered by Intelligence.",description}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
