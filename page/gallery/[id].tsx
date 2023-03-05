import { NextPage, NextPageContext } from "next";
import { useRouter } from "next/router";
import React from "react";
import { Button } from "react-bootstrap";
import { getPageReq } from "../../../api/page";
import Gallery from "../../../components/Gallery";
import { InfoPage } from "../../../components/InfoPage";
import { Title } from "../../../components/Title";

interface PageProps {
    page?: any,
    error?: any
}

const PageGallery: NextPage<PageProps> = ({page}) => {
    const router = useRouter()
    const handleCLickBack = () => {
        router.back()
    }
    return (
        <>
            <InfoPage paddingTop="10px">
                <Button variant="outline-light" onClick={handleCLickBack}>Назад</Button>
                <Title align="center">Галлерея</Title>
                
                <Gallery pictures={page.pictures} videos={page.videos}/>
            </InfoPage>
        </>
    )
}

PageGallery.getInitialProps = async (ctx: NextPageContext) => {
    let page: any = {}
    await getPageReq({ page: ctx.query.id }).then((res: any)=>  {
        page = res.data.page
    });
    return { 
        page
    }
}


export default PageGallery