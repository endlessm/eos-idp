def oidc_userinfo(claims, user):
    """Add claims to OpenID Connect userinfo"""
    # Tell relying parts to re-use the local username if possible
    claims['preferred_username'] = getattr(user, 'username', None)

    return claims
