import { NextPage } from "next"
import { ChangeEvent, useEffect, useRef, useState } from "react"
import { Container } from "react-bootstrap"
import { SupportingForm } from "../../components/Forms/Supporting"
import { CabinetNavbar } from "../../components/Navbars/CabinetNavbar"
import { Title } from "../../components/Title"

const Support: NextPage = () => {


    return (
        <>
            <CabinetNavbar/>
            <Container>
                <Title align="center">Техподдержка</Title>
                <SupportingForm/>
            </Container>
        </>
    )
} 
export default Support