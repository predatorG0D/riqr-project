import { GetServerSideProps, NextPage } from "next"
import { useEffect, useState } from "react"
import { Container } from "react-bootstrap"
import { getUserReq } from "../../api/user"
import { CabinetNavbar } from "../../components/Navbars/CabinetNavbar"
import { PersonalArea } from "../../components/PersonalArea"
import { Title } from "../../components/Title"
import { getCookie } from "../../utils/cookies"
import styles from './style.module.scss'


const Cabinet: NextPage = ({user}: any) => {
    return (
        <>
            <CabinetNavbar/>
            <Container className={styles.container}>
                <Title align="center">Личный кабинет</Title>
                {user? <PersonalArea user={user}/> : null}
            </Container>
        </>
    )
}

export const getServerSideProps: GetServerSideProps = async (ctx) => {
    let data = {};
    await getUserReq({cookie: ctx.req.headers.cookie}).then((res: any) => {
        data = res.data;
    });
    console.log(data);
    if(!data) return {
        redirect: {
            destination: '/',
            permanent: false,
        }
    }
    return {
        props: {
            user: data
        }
    }
}


export default Cabinet