import { NextPage } from "next"
import { useRouter } from 'next/router'
import { Container } from "react-bootstrap"
import { getPageReq, updatePageReq } from "../../../api/page"
import { PageForm } from "../../../components/Forms/PageForm"
import { CabinetNavbar } from "../../../components/Navbars/CabinetNavbar"
import { Title } from "../../../components/Title"
import { useAlertContext } from "../../../contexts/alert"
import backIcon from '../../../public/icons/back.svg'
import styles from './style.module.scss'

interface UpdatePageProps {
    page: any,
    id: string | string[] | undefined
}

const Update: NextPage<UpdatePageProps> = ({page, id}) => {
    const alert = useAlertContext();
    const router = useRouter();
    const handleBack = () => router.back()

    const handleUpdatePage = (data: any) => {
        return updatePageReq({page: {...data, id} }).then((res: any) => {
            router.push('/cabinet/pages');
            alert.setState({isShow: true, isSuccess: true, text: 'Изменения успешно сохранены'})
        }).catch(() => {
            alert.setState({isShow: true, isSuccess: false, text: 'Не получилось изменить страницу'})
        })
    }

    return (
        <>
            <CabinetNavbar/>
            <Container>
                <button onClick={handleBack} className={styles.btn}>
                    <img src={backIcon.src}/>
                    Назад
                </button>
                <Title>Изменение странички</Title>
                <PageForm onSubmit={handleUpdatePage} page={page}/>
            </Container>
        </>
    )
}

Update.getInitialProps = async (ctx) => {
    let page: any = {}
    await getPageReq({ page: ctx.query.id }).then((res: any)=>  {
        page = res.data.page
    });
    return { 
        page,
        id: ctx.query.id
    }
}

export default Update