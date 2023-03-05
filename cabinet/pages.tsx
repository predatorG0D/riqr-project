import { GetServerSideProps, NextPage } from "next"
import { Container } from "react-bootstrap"
import { getPagesReq } from "../../api/page"
import { ModalPay } from "../../components/Modals/ModalPay"
import { CabinetNavbar } from "../../components/Navbars/CabinetNavbar"
import { PagesList } from "../../components/PagesList"

const Pages: NextPage = ({pages}: any) => {
    console.log(pages)
    return (
        <>
            <CabinetNavbar/>
            <Container>
                <PagesList pages={pages}/>
            </Container>
            <ModalPay/>
        </>
    )
}

export const getServerSideProps: GetServerSideProps = async (ctx) => {
    let data: any = [];
    await getPagesReq({cookie: ctx.req.headers.cookie}).then((res: any) => {
        data = res.data.pages.sort((a: any, b: any) => a.id < b.id? 1 : -1);
    });
    return {
        props: {
            pages: data
        }
    }
}


export default Pages