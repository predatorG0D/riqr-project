import { NextPage, NextPageContext } from "next";
import { useRouter } from "next/router";
import { Button } from "react-bootstrap";
import { useSelector } from "react-redux";
import { getPageReq } from "../../api/page";
import { TransitionGallery } from "../../components/Gallery/Transition";
import { InfoPage } from "../../components/InfoPage";
import { Map } from "../../components/Map";
import { AboutPeople } from "../../components/Page/AboutPeople";
import { Biography } from "../../components/Page/Biography";
import { QrCode } from "../../components/QrCode";
import styles from "./style.module.scss"

interface PageProps {
    page?: any,
    id: string | string[] | undefined,
    error?: any
}

const Page: NextPage<PageProps> = ({page, id}) => {

    const router = useRouter();
    const isLoggedIn = useSelector((state: any) => state.auth.isLoggedIn);

    const handleBack = () => {
        if(isLoggedIn) {
            router.back()
        }
        return
    }
    
    const haveMedia = page.pictures.length || page.videos.length;
    console.log(haveMedia)
    console.log(page)
    return (
        <>
            <InfoPage>
                <Button className={styles.button} variant="outline-light" onClick={handleBack}>Назад</Button>
                <Biography user={page}/>
                <AboutPeople user={page}/>
                {haveMedia && <TransitionGallery 
                    pictures={page.pictures} 
                    videos={page.videos}
                    idGallery={id}/>}
                <div>
                    <p className={styles.map_title}>Смотреть на карте:</p>
                    <Map coordinates={page?.coords}/>
                </div>
                <QrCode qrCodes={page.qr_code}/>
            </InfoPage>
        </>
    )
}

Page.getInitialProps = async (ctx: NextPageContext) => {
    let page: any = {}
    await getPageReq({ page: ctx.query.id }).then((res: any)=>  {
        page = res.data.page
    });
    return { 
        page,
        id: ctx.query.id
    }
}

export default Page
