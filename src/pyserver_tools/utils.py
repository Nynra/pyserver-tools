from django.contrib.auth.models import Group, Permission


def force_recreate_group(
    self, group_name: str, verbose: bool = False, raise_exceptions: bool = True
) -> ...:
    """Force delete and recreate a group.

    This function is meant to be used with a django management command but
    can be used in other places as well.

    .. warning::
        This will delete the group and all its permissions. It will then recreate the group
        group without members or permissions.

    Parameters
    ----------
    group_name : str
        The name of the group to delete and recreate.
    verbose : bool
        Whether to print verbose output to the console.
    raise_exceptions : bool
        Whether to raise exceptions when an error occurs.

    Raises
    ------
    ValueError
        If the group does not exist and raise_exceptions is True.
    """
    if not isinstance(group_name, str):
        if raise_exceptions:
            raise TypeError(f"Expected str, got {type(group_name)}")
        return
    if not isinstance(verbose, bool):
        if raise_exceptions:
            raise TypeError(f"Expected bool, got {type(verbose)}")
        return
    if not isinstance(raise_exceptions, bool):
        if raise_exceptions:
            raise TypeError(f"Expected bool, got {type(raise_exceptions)}")
        return

    # Check if the group exists
    if not Group.objects.filter(name=group_name).exists():
        if not raise_exceptions:
            if verbose:
                self.stdout.write(f"Group {group_name} does not exist")
            return
        raise ValueError(f"Group {group_name} does not exist")

    # Delete the group
    group = Group.objects.get(name=group_name)
    group.delete()

    if verbose:
        self.stdout.write(f"Group {group_name} deleted")


def create_group(
    self,
    group_name: str,
    permissions: list,
    force: bool = False,
    verbose: bool = False,
    raise_exceptions: bool = True,
) -> ...:
    """Create a group with the given permissions.

    Parameters
    ----------
    group_name : str
        The name of the group to create.
    permissions : list
        The list of permissions to add to the group.
    force : bool
        Whether to force clear the permissions of the group before adding the new permissions.
    verbose : bool
        Whether to print verbose output to the console.
    raise_exceptions : bool
        Whether to raise exceptions when an error occurs.
    """
    if not isinstance(group_name, str):
        raise TypeError(f"Expected str, got {type(group_name)}")
    if not isinstance(permissions, list):
        raise TypeError(f"Expected list, got {type(permissions)}")
    if not isinstance(force, bool):
        raise TypeError(f"Expected bool, got {type(force)}")
    if not isinstance(verbose, bool):
        raise TypeError(f"Expected bool, got {type(verbose)}")
    if not isinstance(raise_exceptions, bool):
        raise TypeError(f"Expected bool, got {type(raise_exceptions)}")

    # Check if the group exists
    group, created = Group.objects.get_or_create(name=group_name)

    if created and verbose:
        # New group created
        self.stdout.write(f"Group {group_name} created")
    elif created and not verbose:
        # New group created
        pass
    elif not created and force:
        # Force clear the permissions of the existing group
        group.permissions.clear()
        if verbose:
            self.stdout.write(
                f"Group {group_name} permissions cleared because of force"
            )
    else:
        # Group already exists and force is False
        if raise_exceptions:
            raise ValueError(f"Group {group_name} already exists")
        if verbose:
            self.stdout.write(f"Group {group_name} already exists")
        return

    # Set the permissions for the group
    for codename in permissions:
        # Check if the permission exists
        try:
            permission = Permission.objects.get(codename=codename)
        except Permission.DoesNotExist:
            if raise_exceptions:
                raise ValueError(f"Permission {codename} does not exist")
            if verbose:
                self.stderr.write(f"Permission {codename} does not exist")
            continue

        # Add the permission to the group
        group.permissions.add(permission)
        if verbose:
            self.stdout.write(f"Added permission {codename} to group {group_name}")

    if verbose:
        self.stdout.write(f"Group {group_name} permissions updated")
