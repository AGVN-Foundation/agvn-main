import React from 'react'
import Cookies from 'universal-cookie'

export interface AuthProps {
    loginProp: any
    logoutProp: any
    effectFn?: any
}

/**
 * Auth component -> NOTE: may need to just copy and paste this for now since due to problems with the effect function
 */
function Auth({ loginProp, logoutProp, effectFn }: AuthProps) {
    const cookies = new Cookies()
    const [auth, setAuth] = React.useState(false)

    React.useEffect(() => {
        setAuth(cookies.get('token')? true: false)
        if (auth) effectFn()
    }, [])

    return (
        <>
            {auth ? loginProp : logoutProp}
        </>
    )
}

export default Auth