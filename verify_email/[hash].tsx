import { NextPage } from "next";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { verifyEmail } from "../../redux/actions/auth";

interface VerifyEmailProps {
    hash: string | string[] | undefined;
}

const VerifyEmail: NextPage<VerifyEmailProps> = ({ hash }) => {
    const dispatch = useDispatch();
    useEffect(()=> {
        dispatch(verifyEmail(hash));
    }, [])
    return (
        <>
        </>
    )
}

VerifyEmail.getInitialProps = async (ctx) => {
    return {
        hash: ctx.query.hash
    }
}

export default VerifyEmail