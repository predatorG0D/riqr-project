import { NextPage } from "next"
import { useRouter } from "next/router"
import { Container } from "react-bootstrap"
import { createPageReq } from "../../api/page"
import { PageForm } from "../../components/Forms/PageForm"
import { CabinetNavbar } from "../../components/Navbars/CabinetNavbar"
import { Title } from "../../components/Title"
import { useAlertContext } from "../../contexts/alert"

const Create: NextPage = () => {
    const alert = useAlertContext();
    const router = useRouter();

    const handleCreatePage = (data: any) => {
        return createPageReq({page: data}).then((res: any)=> {
            alert.setState({isShow: true, isSuccess: true, text: 'Cтраница успешно создана'})
            router.push(`/page/${res.data.id}`);
        }).catch(()=> {
            alert.setState({isShow: true, isSuccess: false, text: 'Не получилось создать страницу'})
        })
    }

    return (
        <>
            <CabinetNavbar/>
            <Container>
                <Title align="center">Добавление страницы</Title>
                <PageForm onSubmit={handleCreatePage}/>
            </Container>
        </>
    )
}



export default Create